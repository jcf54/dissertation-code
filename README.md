# RegOps demo

**NOTE**: the pipeline was designed for GitLab, and will not work on GitHub Actions. The pipeline is also designed to run on a private GitLab instance, and may or may not work on SaaS GitLab.

This is my test repository for my final year dissertation project. The goal is to use this in our production applications.

It works by reading docstrings from every file in the `app` directory and pulling out hazard cases. This data is then used to generate a hazard log, which is a requirement for DCB0129 and DCB0160. Additionally, it can pull the initial hazard log entries from `app/crm/initial_hazard_log.yaml`, as to satisfy initial hazard requirements for both DCB0129 and DCB0160.

## DCB0129 - [download from source](https://digital.nhs.uk/binaries/content/assets/website-assets/isce/dcb0129/0129242018spec.pdf)

### In-scope requirements only

| Section | Description | Notes |
| --- | --- | --- |
| 2.5 | Third party products | Yes, Python requirements could count |
| 3.1 | Clinical risk management file | Yes, Includes all documentation generated |
| 3.2 | Clinical risk management plan | Yes, this includes the remediations from the hazard log |
| 3.3 | Hazard log | Yes |
| 3.4 | Clinical safety case | Yes, outlines what makes it safe |
| 3.5 | Clinical safety case reports | Yes, explains why it is safe |
| 4.3 | Identification of hazards to patients | Yes, hazard log |
| 4.4 | Estimation of clinical risks | Yes, calculated in hazard log |
| 5.1 | Initial clinical risk evaluation | Yes, included in hazard log |
| 6.1 | Clinical risk control option analysis | Yes, calculated in hazard log |
| 6.2 | Clinical risk benefit analysis | Yes, aided by hazard log |
| 6.3 | Implementation of clinical risk control measures | Yes, aided by design of hazard log |
| 6.4 | Completeness of clinical risk control | Yes, aided by design of hazard log |
| 7.3 | Modification | Yes, satisfied due to CI workflow and git repository for auditing previous versions of documentation |

## DCB0160 - [download from source](https://digital.nhs.uk/binaries/content/assets/website-assets/data-and-information/information-standards/standards-and-collections/dcb0160/0160252018spec.pdf)

### In-scope requirements only

| Section | Description | Relevance |
| --- | --- | --- |
| 2.6 | Third party products | Yes, Python requirements could count |
| 3.1 | Clinical risk management file | Yes, includes all documentation generated |
| 3.2 | Clinical risk management plan | Yes, unsure how currently |
| 3.3 | Hazard log | Yes |
| 3.4 | Clinical safety case | Yes, proof it's safe - test reports, etc |
| 3.5 | Clinical safety case reports | Yes, proof it's safe - test reports, etc |
| 4.2 | Health IT system scope definition | Must be defined beforehand |
| 4.3 | Identification of hazards to patients | Yes, hazard log |
| 4.4 | Estimation of clinical risks | Yes, hazard log |
| 5.1 | Initial clinical risk evaluation | Yes, hazard log |
| 6.1 | Clinical risk control option analysis | Yes, aided by hazard log |
| 6.2 | Clinical risk benefit analysis | Yes, hazard log |
| 6.3 | Implementation of clinical risk control measures | Yes, aided by design of hazard log |
| 6.4 | Completeness of clinical risk control | Yes, aided by design of hazard log |
| 7.3 | Maintenance | Yes, satisfied due to CI workflow and git repository for auditing previous versions of documentation |

## Cumulative requirements

| Title | Description | Relevance |
| --- | --- | --- |
| Third party products | Any third party product used must be assessed | Yes, Python requirements could count |
| Clinical risk management file | Must be maintained throughout the product's lifecycle (CI) | Yes, Includes all documentation generated |
| Clinical risk management plan | Must be maintained throughout the product's lifecycle (CI) | Yes, this includes the remediations from the hazard log |
| Hazard log | Must be maintained for every change (CI) | Yes |
| Clinical safety case | Outlines what makes the application safe | Yes, outlines what makes it safe |
| Clinical safety case reports | Outlines why the application is safe | Yes, explains why it is safe |
| Identification of hazards to patients | The hazard log identifies any hazards, including those against patients  | Yes, hazard log |
| Estimation of clinical risks | Clinical risk calculations happen automatically in the hazard log | Yes, calculated in hazard log |
| Initial clinical risk evaluation | The ability to add clinical risks initially is supported | Yes, included in hazard log |
| Clinical risk control option analysis | Acceptability of risk is not calculated in the hazard log, however risk values that raise questions about acceptability are | Yes, calculated in hazard log |
| Clinical risk benefit analysis | Acceptability of risk is not calculated in the hazard log, however risk values that raise questions about acceptability are | Yes, aided by hazard log |
| Implementation of clinical risk control measures | This is helped by the design of the hazard log integrator, in that they're added to functions. Would be resolved by implementing code reviews | Yes, aided by design of hazard log |
| Completeness of clinical risk control | Would be resolved by implementing code reviews | Yes, aided by design of hazard log |
| Modification | On each edit, the documentation is regenerated. As such it's always up-to-date so long as it's used correctly. Additionally, documentation is pushed to another git repository to allow auditing and version control | Yes, satisfied due to CI workflow and git repository for auditing previous versions of documentation |

## Features required (by DCB0129 and DCB0160)

### Implementation

Security, code quality, and application assurance is run on all branches, and checked on merge requests. This ensures that the application meets the set critera at each step in development before it's merged to the main branch and deployed. This meets a key component on the risk management process, in that it ensures that the application is safe at each step in development.

Artifact generation is done only on the main branch, before deployment. This ensures that the artifacts are always up-to-date with the latest version of the application, and that they're always available for auditing.

Using GitLab's CI pipelines allow for the generation of artifacts, as well as the ability to comprehensively review code changes before they're merged while presented with changes in code quality or testing. For example, the reviewer is notified on the merge page if code quality is better or worse, or if testing coverage has increased or decreased. This allows for a more comprehensive review of code changes, and helps to ensure that the application is safe.

### Hazard log

The hazard log is a mechanism for recording ongoing identification and resolution of hazards associated with a specific system in a specific use case. It's a key part to the risk management process and provides the foundation for many of the requirements.

It's designed so that it's tightly integrated with the codebase, so it's very easy for developers to add hazards as development progresses. To add a hazard to the hazard log, very simple add the relevant details in the function/class' docstring. The hazard log is automatically generated from the docstrings in the codebase by the CI pipelines. Enforcing the hazards defined in the docstrings are actually actions should be done through code reviews, and it will ensure that the hazards are mitigated correctly.

### Interpretation of `requirements.txt`

To ensure that all third party libraries are assessed, the `requirements.txt` is parsed for comments. Comments (lines starting with #) are stored and indexed in a dictionary against the library's name. This is then used to generate a report of all third party libraries used along with their defenses (why they were used, why they are safe, etc). This is included in the clinical safety case report as evidence.

### Interpretation of test/code coverage reports

To ensure the application is safe and meets all assurances set, all outcomes from testing tools are stored as artifacts and are parsed by the CI pipeline. This is used to generate evidence that the application is safe and meets all assurances set. This is included in the clinical safety case report as evidence.

## Definitions

| Term | Definition |
| --- | --- |
| Clinical risk management file | Repository of all records and other documents that are produced by the clinical risk management process. |
| Clinical risk management plan | A plan which documents how the Manufacturer will conduct clinical risk management of a Health IT System |
| Clinical safety case | Accumulation and organisation of product and business process documentation and supporting evidence, through the lifecycle of a Health IT System.
| Clinical safety case report | A report that presents the arguments and supporting evidence that provides a compelling, comprehensible and valid case that a system is safe for a given application in a given environment at a defined point in a Health IT System’s lifecycle. |
| Hazard log | A mechanism for recording and communicating the on-going identification and resolution of hazards associated with a Health IT System. |
| Safety Incident Management Log | Tool to record the reporting, management and resolution of safety incidents associated with a Health IT System. |

## Errors

- CI pipeline unpredictable returns `fatal: shallow file has changed since we read it`.
