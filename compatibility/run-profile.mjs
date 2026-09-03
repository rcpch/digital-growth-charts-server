import { spawnSync } from 'node:child_process';
import {
  copyFileSync,
  existsSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const COMPATIBILITY_DIR = dirname(fileURLToPath(import.meta.url));
const CACHE_DIR = process.env.COMPATIBILITY_CACHE_DIR || '/cache';
const RESULTS_DIR = process.env.COMPATIBILITY_RESULTS_DIR || '/results';
const LOCAL_COMPONENT_REPOSITORY = '/local-component-repository';
const REQUEST_TIMEOUT_MS = 60_000;

const profilesDocument = JSON.parse(readFileSync(join(COMPATIBILITY_DIR, 'profiles.json'), 'utf8'));
const scenarios = JSON.parse(readFileSync(join(COMPATIBILITY_DIR, 'scenarios.json'), 'utf8'));

function usage() {
  console.log(`Usage: s/compatibility-test [--profile ID] [--keep]

Options:
  --profile ID   Run one declared compatibility profile (default: all supported profiles)
  --keep         Keep temporary component checkouts in the compatibility cache
  --list         List declared profiles without running them
  --help         Show this help

Set COMPATIBILITY_API_BASE_URL to test an API other than the Compose growth-api service.`);
}

function parseArgs(args) {
  const options = { profileId: undefined, keep: false, list: false };
  for (let index = 0; index < args.length; index += 1) {
    const argument = args[index];
    if (argument === '--help') {
      usage();
      process.exit(0);
    }
    if (argument === '--keep') {
      options.keep = true;
      continue;
    }
    if (argument === '--list') {
      options.list = true;
      continue;
    }
    if (argument === '--profile') {
      options.profileId = args[index + 1];
      index += 1;
      if (!options.profileId) throw new Error('--profile requires an ID');
      continue;
    }
    if (argument.startsWith('--profile=')) {
      options.profileId = argument.slice('--profile='.length);
      continue;
    }
    throw new Error(`Unknown argument: ${argument}`);
  }
  return options;
}

function run(command, args, options = {}) {
  console.log(`$ ${command} ${args.join(' ')}`);
  const result = spawnSync(command, args, {
    cwd: options.cwd,
    env: options.env || process.env,
    encoding: 'utf8',
    stdio: options.capture ? 'pipe' : 'inherit',
  });
  if (result.error) throw result.error;
  if (result.status !== 0) {
    const details = options.capture ? `\n${result.stderr || result.stdout}` : '';
    throw new Error(`${command} exited with status ${result.status}${details}`);
  }
  return result.stdout?.trim();
}

function validateProfiles() {
  if (profilesDocument.schemaVersion !== 1 || !Array.isArray(profilesDocument.profiles)) {
    throw new Error('compatibility/profiles.json has an unsupported schema');
  }
  const ids = new Set();
  for (const profile of profilesDocument.profiles) {
    if (!profile.id || ids.has(profile.id)) throw new Error(`Invalid or duplicate profile ID: ${profile.id}`);
    ids.add(profile.id);
    if (!['supported', 'deprecated', 'retired'].includes(profile.status)) {
      throw new Error(`${profile.id} has unsupported status ${profile.status}`);
    }
    if (!/^\d{4}-\d{2}-\d{2}$/.test(profile.reviewAfter || '')) {
      throw new Error(`${profile.id} must declare a reviewAfter date`);
    }
    if (profile.status === 'deprecated' && !/^\d{4}-\d{2}-\d{2}$/.test(profile.sunset || '')) {
      throw new Error(`${profile.id} must declare a sunset date when deprecated`);
    }
    if (!/^[0-9a-f]{40}$/.test(profile.component?.revision || '')) {
      throw new Error(`${profile.id} must pin a full component Git revision`);
    }
    if (!profile.component.repository) throw new Error(`${profile.id} has no component repository`);
  }
}

const referenceToCamelCase = (reference) =>
  reference.replace(/-([a-z0-9])/g, (_, character) => character.toUpperCase()).replace(/-/g, '');
const capitalise = (value) => value.charAt(0).toUpperCase() + value.slice(1);
const expectedProvenanceReference = (reference) => (reference === 'turner' ? 'turners-syndrome' : reference);

function buildJobs() {
  const jobs = [];
  for (const matrix of scenarios.series.matrices) {
    for (const sex of matrix.sexes) {
      for (const method of matrix.methods) {
        jobs.push({
          name: `${referenceToCamelCase(matrix.reference)}${capitalise(sex)}${capitalise(method)}`,
          description: `${matrix.reference} ${sex} ${method}`,
          reference: matrix.reference,
          endpoint: scenarios.series.endpoint,
          body: { ...scenarios.series.body, measurement_method: method, sex },
          allowDuplicates: false,
        });
      }
    }
  }
  for (const special of scenarios.special) jobs.push({ allowDuplicates: false, ...special });
  const names = jobs.map(({ name }) => name);
  if (new Set(names).size !== names.length) throw new Error('Compatibility scenario names must be unique');
  return jobs;
}

async function waitForApi(baseUrl) {
  let lastError;
  for (let attempt = 1; attempt <= 60; attempt += 1) {
    try {
      const response = await fetch(`${baseUrl}/`, { signal: AbortSignal.timeout(2_000) });
      if (response.ok) return response;
      lastError = new Error(`HTTP ${response.status}`);
    } catch (error) {
      lastError = error;
    }
    await new Promise((resolve) => setTimeout(resolve, 1_000));
  }
  throw new Error(`API did not become ready at ${baseUrl}`, { cause: lastError });
}

async function post(baseUrl, job) {
  const response = await fetch(`${baseUrl}/${job.reference}/${job.endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(job.body),
    signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
  });
  const text = await response.text();
  let body;
  try {
    body = JSON.parse(text);
  } catch {
    throw new Error(`${job.name} returned non-JSON HTTP ${response.status}: ${text.slice(0, 500)}`);
  }
  if (!response.ok) throw new Error(`${job.name} returned HTTP ${response.status}: ${text.slice(0, 500)}`);
  return body;
}

function measurementsFromResponse(endpoint, response) {
  if (endpoint === 'fictional-child-data') return Array.isArray(response) ? response : [];
  if (endpoint === 'calculation') return response ? [response] : [];
  if (endpoint === 'bulk-calculation') {
    const results = response?.results || [];
    const measurements = results.filter((result) => result?.plottable_data);
    if (measurements.length !== results.length) {
      throw new Error(`bulk-calculation returned ${results.length - measurements.length} error result(s)`);
    }
    return measurements;
  }
  throw new Error(`Unsupported compatibility endpoint: ${endpoint}`);
}

function validateProvenance(measurements, job, apiRevision) {
  const expectedReference = expectedProvenanceReference(job.reference);
  let engineIdentity;
  let engine;
  for (const [index, measurement] of measurements.entries()) {
    const provenance = measurement?.provenance;
    if (provenance?.growth_reference !== expectedReference) {
      throw new Error(
        `${job.name}[${index}] provenance is ${provenance?.growth_reference}, expected ${expectedReference}`,
      );
    }
    const candidate = provenance.calculation_engine;
    if (
      candidate?.name !== 'rcpchgrowth' ||
      !candidate.version ||
      !/^[0-9a-f]{40}$/.test(candidate.commit || '')
    ) {
      throw new Error(`${job.name}[${index}] has invalid calculation-engine provenance`);
    }
    const apiServer = provenance.api_server;
    if (
      apiServer?.name !== 'digital-growth-charts-server' ||
      !apiServer.version ||
      apiServer.commit !== apiRevision
    ) {
      throw new Error(`${job.name}[${index}] has invalid API-server provenance`);
    }
    const identity = `${candidate.name}@${candidate.version}#${candidate.commit}`;
    if (engineIdentity && identity !== engineIdentity) {
      throw new Error(`${job.name} contains measurements from different calculation engines`);
    }
    engineIdentity = identity;
    engine = candidate;
  }
  return { identity: engineIdentity, ...engine };
}

async function fetchCandidateResponses(baseUrl) {
  const rootResponse = await waitForApi(baseUrl);
  const apiRevision = rootResponse.headers.get('x-git-revision') || 'local-unversioned';
  if (apiRevision === 'local-unversioned') {
    console.warn('Candidate API did not expose X-Git-Revision; recording it as local-unversioned.');
  }

  const cases = [];
  const casesByName = new Map();
  let sharedEngine;
  for (const job of buildJobs()) {
    const response = await post(baseUrl, job);
    const measurements = measurementsFromResponse(job.endpoint, response);
    if (measurements.length === 0) throw new Error(`${job.name} returned no measurements`);
    const engine = validateProvenance(measurements, job, apiRevision);
    if (sharedEngine && engine.identity !== sharedEngine.identity) {
      throw new Error(`${job.name} used ${engine.identity}, but earlier cases used ${sharedEngine.identity}`);
    }
    sharedEngine = engine;
    const testCase = {
      id: job.name,
      title: `Compatibility: ${job.name}`,
      reference: job.reference,
      sex: job.body.sex,
      measurementMethod: job.body.measurement_method,
      chartType: 'centile',
      allowDuplicates: job.allowDuplicates,
      measurements: { [job.body.measurement_method]: measurements },
    };
    cases.push(testCase);
    casesByName.set(job.name, testCase);
    process.stdout.write('.');
  }
  process.stdout.write('\n');

  const sdsMeasurements = {};
  for (const method of ['height', 'weight', 'bmi', 'ofc']) {
    const source = casesByName.get(`ukWhoFemale${capitalise(method)}`);
    if (!source) throw new Error(`Missing UK-WHO female ${method} source for the SDS compatibility case`);
    sdsMeasurements[method] = source.measurements[method];
  }
  cases.push({
    id: 'ukWhoFemaleMultipleMethodSds',
    title: 'Compatibility: UK-WHO female multiple-method SDS',
    reference: 'uk-who',
    sex: 'female',
    measurementMethod: 'height',
    chartType: 'sds',
    allowDuplicates: false,
    measurements: sdsMeasurements,
  });

  return {
    generatedAt: new Date().toISOString(),
    api: { baseUrl, revision: apiRevision },
    calculationEngine: {
      name: sharedEngine.name,
      version: sharedEngine.version,
      commit: sharedEngine.commit,
    },
    cases,
  };
}

function localRepositoryContains(revision) {
  if (!existsSync(LOCAL_COMPONENT_REPOSITORY)) return false;
  const result = spawnSync(
    'git',
    [
      '-c',
      `safe.directory=${LOCAL_COMPONENT_REPOSITORY}`,
      '-C',
      LOCAL_COMPONENT_REPOSITORY,
      'cat-file',
      '-e',
      `${revision}^{commit}`,
    ],
    { stdio: 'ignore' },
  );
  return result.status === 0;
}

function runProfile(profile, payload, keep) {
  const runRoot = mkdtempSync(join(CACHE_DIR, `${profile.id}-`));
  const checkout = join(runRoot, 'component');
  const repository = localRepositoryContains(profile.component.revision)
    ? LOCAL_COMPONENT_REPOSITORY
    : profile.component.repository;
  console.log(`\n=== ${profile.id} (${profile.component.revision}) ===`);
  console.log(`Component source: ${repository}`);

  try {
    if (repository === LOCAL_COMPONENT_REPOSITORY) {
      // `git clone` starts an upload-pack subprocess which does not inherit
      // command-scoped safe.directory values, so configure this throwaway container globally.
      run('git', ['config', '--global', '--add', 'safe.directory', LOCAL_COMPONENT_REPOSITORY]);
      run('git', ['config', '--global', '--add', 'safe.directory', `${LOCAL_COMPONENT_REPOSITORY}/.git`]);
    }
    run('git', ['clone', '--no-checkout', repository, checkout]);
    run('git', ['checkout', '--detach', profile.component.revision], { cwd: checkout });
    run('npm', ['ci', '--no-audit', '--no-fund'], {
      cwd: checkout,
      env: { ...process.env, npm_config_cache: join(CACHE_DIR, 'npm') },
    });

    copyFileSync(join(COMPATIBILITY_DIR, 'consumer.test.tsx'), join(checkout, 'src', 'compatibility.generated.test.tsx'));
    writeFileSync(
      join(checkout, 'src', 'compatibility.generated.responses.json'),
      `${JSON.stringify(payload)}\n`,
    );

    run(
      'npm',
      ['test', '--', '--runInBand', '--runTestsByPath', 'src/compatibility.generated.test.tsx'],
      {
        cwd: checkout,
        env: {
          ...process.env,
          CI: 'true',
          COMPATIBILITY_PROFILE_ID: profile.id,
          COMPATIBILITY_PROVENANCE_SUPPORT: String(profile.provenanceSupport),
        },
      },
    );
    writeFileSync(
      join(RESULTS_DIR, `${profile.id}.json`),
      `${JSON.stringify({ profile, status: 'passed', api: payload.api, calculationEngine: payload.calculationEngine }, null, 2)}\n`,
    );
  } catch (error) {
    writeFileSync(
      join(RESULTS_DIR, `${profile.id}.json`),
      `${JSON.stringify({ profile, status: 'failed', error: error.message, api: payload.api }, null, 2)}\n`,
    );
    throw error;
  } finally {
    if (keep) {
      console.log(`Kept temporary checkout at ${runRoot}`);
    } else {
      rmSync(runRoot, { recursive: true, force: true });
    }
  }
}

async function main() {
  validateProfiles();
  const options = parseArgs(process.argv.slice(2));
  if (options.list) {
    for (const profile of profilesDocument.profiles) {
      console.log(`${profile.id}\t${profile.status}\t${profile.component.revision}`);
    }
    return;
  }

  const selectedProfiles = profilesDocument.profiles.filter(
    (profile) =>
      profile.status !== 'retired' && (!options.profileId || profile.id === options.profileId),
  );
  if (selectedProfiles.length === 0) throw new Error(`Unknown active profile: ${options.profileId}`);

  mkdirSync(CACHE_DIR, { recursive: true });
  mkdirSync(RESULTS_DIR, { recursive: true });
  const apiBaseUrl = (process.env.COMPATIBILITY_API_BASE_URL || 'http://growth-api:8000').replace(/\/$/, '');
  console.log(`Fetching candidate responses from ${apiBaseUrl}`);
  const payload = await fetchCandidateResponses(apiBaseUrl);
  writeFileSync(join(RESULTS_DIR, 'candidate-responses.json'), `${JSON.stringify(payload, null, 2)}\n`);
  console.log(
    `Candidate API ${payload.api.revision}; ${payload.calculationEngine.name} ${payload.calculationEngine.version} (${payload.calculationEngine.commit})`,
  );
  console.log(`${payload.cases.length} compatibility cases; ${selectedProfiles.length} component profile(s)`);

  const failures = [];
  for (const profile of selectedProfiles) {
    try {
      runProfile(profile, payload, options.keep);
    } catch (error) {
      failures.push(`${profile.id}: ${error.message}`);
    }
  }
  if (failures.length > 0) throw new Error(`Compatibility matrix failed:\n${failures.join('\n')}`);
  console.log('\nCompatibility matrix passed.');
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exitCode = 1;
});
