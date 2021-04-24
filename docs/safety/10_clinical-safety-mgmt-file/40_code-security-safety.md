---
title: Deployment Security
reviewers: Dr Marcus Baw
---

# 'Code Chain'

In order to maintain security and safety, while still enabling 'agile' software development practices, we have carefully built a DevOps (Developer Operations) strategy which is consistent with industry best practice yet is frictionless in practice and therefore easy to comply with.

These practices ensure tight security of the code, restricting deployment to the live environment. These security practices are in operation in every part of the 'code chain' from writing the code through to deployment on the live server, and each of the many steps in between.

Also within these practices are measures which ensure that the code which is deployed is tested, safe, and does not contain regressions (changes which break a feature)

## GitHub Repository

Security of our GitHub code repositories is exceedingly tight, combining **physical security of devices**, as well as **multi-factor access controls**.

Login to the GitHub organisation is restricted to specific users, who are in the RCPCH Developer Team, who are all required to use **two-factor authentication** (username + password + another factor such as Google Authenticator)

'Pushes' of new code to the GitHub repositories are made using **SSH Keys** which are secure, long, cryptographic tokens held on the computers used to develop the growth charts. Use of the token requires a further password, so possession of the computer alone is not enough to use the computer's SSH key to make a push of unauthorised code to GitHub.

Commits of code are 'signed' using GPG (Gnu Privacy Guard - an open source implementation of the PGP protocol). This is a further attestation to the correct identity of the committer of the code.

## Deployments of the server

Deployment is completely automated, meaning no code can be manually added to our Azure WebApps, before or after deployment.

Security is handled via long cryptographic keys from Microsoft Azure which are known to GitHub but never made public.

GitHub's 'Action' workflow can use this key to authenticate itself to the Microsoft Azure cloud platform, and can push new code from the GitHub repository to the Azure WebApp where it runs as an application and is available as an API.

## Code 'Promotion' Safety Strategy

New code is never deployed to the `live` branch. Safety mechanisms on the relevant branches of our GitHub repositories prevent direct 'pushes' of code. Instead, new features must be developed on the `development` branch or in a branch created specially for that feature.

From `development` or feature branches, code is 'promoted', following successful passing of tests for correct operation, to a `staging` branch, which allows for further testing, and where necessary review and confirmation of interoperation with other components of the dGC products.

Once further user acceptance testing and stability tests are satifsactorily passed, this code can be merged into the `live` branch.

We believe that this strategy reduces the risk of errors being introduced into the API code to a very low level.
