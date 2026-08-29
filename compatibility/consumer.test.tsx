import React from 'react';
import { cleanup, render } from '@testing-library/react';

import RCPCHChart from './RCPCHChart/RCPCHChart';

interface CompatibilityCase {
    id: string;
    title: string;
    reference: string;
    sex: string;
    measurementMethod: string;
    chartType: 'centile' | 'sds';
    allowDuplicates: boolean;
    measurements: Record<string, unknown[]>;
}

interface CompatibilityPayload {
    cases: CompatibilityCase[];
}

const payload = require('./compatibility.generated.responses.json') as CompatibilityPayload;
const provenanceSupport = process.env.COMPATIBILITY_PROVENANCE_SUPPORT === 'true';

jest.setTimeout(120_000);

afterEach(() => cleanup());

const clone = <T,>(value: T): T => JSON.parse(JSON.stringify(value));

function renderCase(testCase: CompatibilityCase) {
    const errors: unknown[][] = [];
    const consoleError = jest.spyOn(console, 'error').mockImplementation((...args) => errors.push(args));

    try {
        const chart = render(
            <RCPCHChart
                title={testCase.title}
                measurementMethod={testCase.measurementMethod as any}
                reference={testCase.reference as any}
                sex={testCase.sex as any}
                measurements={clone(testCase.measurements) as any}
                allowDuplicates={testCase.allowDuplicates}
                midParentalHeightData={{}}
                enableZoom={false}
                chartType={testCase.chartType}
                enableExport={false}
                exportChartCallback={() => undefined}
                clinicianFocus={false}
                theme="monochrome"
                height={800}
                width={1000}
            />,
        );
        return { chart, errors };
    } finally {
        consoleError.mockRestore();
    }
}

function plottedPointCount(chart: ReturnType<typeof render>, testCase: CompatibilityCase) {
    const pointGroups = chart.queryAllByTestId('chronologicalMeasurementPoint');
    if (testCase.chartType === 'centile') return pointGroups.length;
    return pointGroups.reduce((count, group) => count + group.querySelectorAll('path').length, 0);
}

function expectedVisualPointCount(testCase: CompatibilityCase) {
    const coordinates = new Set<string>();
    for (const [method, measurements] of Object.entries(testCase.measurements)) {
        for (const measurement of measurements as any[]) {
            const point = measurement.plottable_data[`${testCase.chartType}_data`].chronological_decimal_age_data;
            coordinates.add(`${method}:${point.x}:${point.y}`);
        }
    }
    return coordinates.size;
}

describe(`API compatibility profile ${process.env.COMPATIBILITY_PROFILE_ID}`, () => {
    test.each(payload.cases)('$id renders candidate API measurements', (testCase) => {
        const { chart, errors } = renderCase(testCase);

        expect(errors).toEqual([]);
        expect(chart.queryByText('The chart could not be displayed')).toBeNull();
        expect(chart.getByText(testCase.title)).not.toBeNull();
        expect(plottedPointCount(chart, testCase)).toBe(expectedVisualPointCount(testCase));
        expect(chart.queryByTestId('provenance-warning-banner')).toBeNull();
    });

    test('profile has its declared provenance capability', () => {
        const source = payload.cases.find(
            (testCase) =>
                testCase.reference === 'uk-who' &&
                testCase.sex === 'female' &&
                testCase.measurementMethod === 'height' &&
                testCase.chartType === 'centile',
        );
        if (!source) throw new Error('Missing UK-WHO female height capability-probe case');

        const mismatchedMeasurement = clone(source.measurements.height[0]) as any;
        mismatchedMeasurement.provenance.growth_reference = 'cdc';
        const { chart, errors } = renderCase({
            ...source,
            id: 'provenance-capability-probe',
            title: 'Provenance capability probe',
            measurements: { height: [mismatchedMeasurement] },
        });

        expect(errors).toEqual([]);
        expect(chart.queryByText('The chart could not be displayed')).toBeNull();
        if (provenanceSupport) {
            expect(plottedPointCount(chart, source)).toBe(0);
            expect(chart.queryByTestId('provenance-warning-banner')).not.toBeNull();
        } else {
            expect(plottedPointCount(chart, source)).toBe(1);
            expect(chart.queryByTestId('provenance-warning-banner')).toBeNull();
        }
    });
});
