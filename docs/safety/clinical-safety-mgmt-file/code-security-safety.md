# 'Code Chain' Clinical Safety

In order to maintain security and safety, while still enabling 'agile' software development practices, we have carefully built a DevOps (Developer Operations) strategy which is consistent with industry best practice yet is frictionless in practice and therefore easy to comply with.

These practices ensure tight security of the code, restricting deployment to the live environment.

Also within these practices are measures which ensure that the code which is deployed is tested, safe, and does not contain regressions (changes which break a feature)

## GitHub Repository

Security of our GitHub code repositories is exceedingly tight, combining physical security of devices, as well as muti-factor access controls.

Login to the GitHub organisation is restricted to specific users in the RCPCH Developer Team, who are all required to use two-factor authentication (username + password + another factor such as Google Authenticator)

'Pushes' of new code to the GitHub repositories are made using SSH Keys which are secure, long, cryptographic tokens held on the computers used to develop the growth charts. Use of the token requires a further password, so possession of the computer alone is not enough.

## Deployments of the server

Deployment is completely automated, no code can be manually added to our WebApps, before or after deployment.

Security is handled via long cryptographic keys from Microsoft Azure which are known to GitHub but never made public.

GitHub's 'Action' workflow can use this key to authenticate itself to the Microsoft Azure cloud platform, and can push new code from the GitHub repository to the Azure WebApp.

## Code 'Promotion' Safety Strategy

New code is never pushed to the `live` branch

Feature development occurs in a feature branch

Once the feature is complete it is merged into a testing branch

Once further user acceptance testing and stability tests are satifsactorily passed, this code can be merged into the live branch

This strategy reduces the risk of errors being introduced into the API code.
