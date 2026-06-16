# Semantic Chunking and Retrieval Test Cases

## Purpose

Use these tests to verify that:

1. Each chunk contains a complete idea instead of unrelated topics.
2. Important facts are not separated from their headings or explanations.
3. Similar documents are not confused with one another.
4. Paraphrased questions retrieve the correct source.
5. The retrieved chunks contain enough context to answer accurately.

## How to Run

1. Run `python ingest.py` to rebuild the vector database.
2. Run `python query.py`.
3. Enter each question from the test cases below.
4. Check the four retrieved chunks against the expected source and facts.
5. Mark a test as passed only when the required source appears and the retrieved text supports the answer.

## Pass Criteria

- **Retrieval pass:** The expected PDF is present in the top four results.
- **Strong retrieval pass:** The expected PDF is the first result.
- **Answer pass:** All required facts are present in the retrieved context.
- **Chunk-quality pass:** The chunk is understandable by itself and does not begin or end with an incomplete sentence, heading, or list.
- **Disambiguation pass:** A similarly worded company document does not outrank the correct company.

## Basic Fact Retrieval

| ID | Question | Expected source | Required answer facts |
|---|---|---|---|
| F01 | Who founded Devsinc and where is its headquarters? | `Devsinc.pdf` | Usman Asif; Lahore, Pakistan |
| F02 | In what year was Devsinc founded? | `Devsinc.pdf` | 2008 according to the founder profile; the document notes some sources say 2009-2010 |
| F03 | How many projects has Devsinc delivered and in how many countries does it operate? | `Devsinc.pdf` | 3,000+ projects; 23+ countries |
| F04 | Who founded Systems Limited and when? | `Systems Limited.pdf` | Aezaz Hussain; 1977 |
| F05 | What is the stock ticker of Systems Limited? | `Systems Limited.pdf` | SYS; Pakistan Stock Exchange |
| F06 | Who is the CEO of Systems Limited? | `Systems Limited.pdf` | Muhammad Asif Peer |
| F07 | When was VertXSoft founded and where is its head office? | `vertxSoft.pdf` | 2022; Johar Town, Lahore, Pakistan |
| F08 | What examination does SkillPass help users prepare for? | `Skill Pass.pdf` | Italian driving theory examination; Patente |
| F09 | What is the name of the SkillPass AI tutor? | `Skill Pass.pdf` | SkillBot |
| F10 | What does OWASP A01:2021 represent? | `OWASP top 10 vulnerabilities.pdf` | Broken Access Control |

## Paraphrase and Semantic Retrieval

These questions avoid copying the exact wording from the PDFs.

| ID | Question | Expected source | Required answer facts |
|---|---|---|---|
| S01 | Which Pakistani technology company is described as the country's first software house? | `Systems Limited.pdf` | Systems Limited; founded in 1977 |
| S02 | Which learning product removes language barriers for people studying for a license in Italy? | `Skill Pass.pdf` | SkillPass; multilingual driving theory preparation |
| S03 | Which company builds RAG systems, AI assistants, and document-processing solutions? | `vertxSoft.pdf` | VertXSoft |
| S04 | Which web security risk lets a user view or change resources beyond their permission? | `OWASP top 10 vulnerabilities.pdf` | Broken Access Control |
| S05 | Which vulnerability can happen when user input is treated as a database query or operating-system command? | `OWASP top 10 vulnerabilities.pdf` | Injection; A03:2021 |
| S06 | Which company was started by Usman Asif and now works across more than 23 countries? | `Devsinc.pdf` | Devsinc |
| S07 | What platform gives learners XP, streaks, leaderboards, and achievement badges? | `Skill Pass.pdf` | SkillPass; gamification system |
| S08 | Which company provides computer-vision solutions for object detection and industrial monitoring? | `vertxSoft.pdf` | VertXSoft |

## Complete-Context Tests

These tests check whether one retrieved chunk contains a heading together with its important explanation or list.

| ID | Question | Expected source | The retrieved context should keep together |
|---|---|---|---|
| C01 | What cloud and DevOps services does Devsinc provide? | `Devsinc.pdf` | Cloud migration, infrastructure management, CI/CD, Kubernetes, consulting, and optimization |
| C02 | What are the four stages of the SkillPass learning journey? | `Skill Pass.pdf` | Learn Theory, Practice Quizzes, Simulate Exams, Take Official Exam |
| C03 | What are the six phases of the VertXSoft development process? | `vertxSoft.pdf` | Discovery, Design, Development, Testing, Deployment, Maintenance |
| C04 | How should organizations mitigate cryptographic failures? | `OWASP top 10 vulnerabilities.pdf` | Strong encryption, encryption at rest and in transit, HTTPS, secure key management |
| C05 | What services are included in Systems Limited's BPO offering? | `Systems Limited.pdf` | Customer support, contact centers, back-office operations, technical support, business process management |
| C06 | Which license categories does SkillPass support? | `Skill Pass.pdf` | Patente B, A, A1, A2, and AM |

## Cross-Page Boundary Tests

`PyPDFLoader` creates one document per page before semantic splitting. Therefore, a semantic chunk cannot cross a PDF page boundary in the current implementation. These tests reveal whether retrieval still obtains both sides of a page break.

| ID | Question | Expected source | Boundary being tested |
|---|---|---|---|
| B01 | Describe Devsinc's company history and its main custom software services. | `Devsinc.pdf` | History continues from page 1 to page 2; custom software starts on page 2 |
| B02 | What are the impacts and mitigations of Broken Access Control? | `OWASP top 10 vulnerabilities.pdf` | Impact starts on page 1 and continues on page 2 before mitigation |
| B03 | Explain SkillPass interactive lessons and exam simulation features. | `Skill Pass.pdf` | Interactive Lessons heading is on page 3; its details are on page 4 |
| B04 | What AI features and technical features does SkillPass provide? | `Skill Pass.pdf` | AI section starts on page 6 and continues on page 7 |
| B05 | Which cloud platforms does Systems Limited support? | `Systems Limited.pdf` | The platform list starts on page 3 and continues with GCP on page 4 |
| B06 | Describe VertXSoft's cloud services and computer-vision services. | `vertxSoft.pdf` | Cloud section starts on page 3 and continues on page 4 |

For these tests, pass only if the top four results collectively contain all required information. A single chunk is not expected to cross the page boundary with the current ingestion design.

## Similar-Document Disambiguation

These are important because Devsinc, Systems Limited, and VertXSoft all mention AI, cloud, web development, mobile development, Docker, Kubernetes, and similar job roles.

| ID | Question | Correct source | Must not be confused with |
|---|---|---|---|
| D01 | Which company is publicly listed under ticker SYS? | `Systems Limited.pdf` | Devsinc or VertXSoft |
| D02 | Which company was founded in 2022 and develops RAG systems? | `vertxSoft.pdf` | Devsinc |
| D03 | Which company reports 3,000+ delivered projects? | `Devsinc.pdf` | Systems Limited |
| D04 | Which company has more than 8,000 employees globally? | `Systems Limited.pdf` | Devsinc |
| D05 | Which company lists 236+ active clients? | `Devsinc.pdf` | Systems Limited |
| D06 | Which company specifically lists computer vision and smart manufacturing applications? | `vertxSoft.pdf` | Devsinc or Systems Limited |
| D07 | Compare the founding years of Devsinc, Systems Limited, and VertXSoft. | All three company PDFs | Devsinc: 2008 with source uncertainty noted; Systems Limited: 1977; VertXSoft: 2022 |
| D08 | Which of the three company profiles describes a public company? | `Systems Limited.pdf` | Devsinc and VertXSoft are described as private |

## OWASP Category Separation

These tests verify that adjacent vulnerability sections are not merged into confusing chunks.

| ID | Question | Expected answer |
|---|---|---|
| O01 | Which OWASP category recommends parameterized queries and input allow-listing? | A03:2021 Injection |
| O02 | Which category recommends threat modeling during application design? | A04:2021 Insecure Design |
| O03 | Which category covers default passwords and exposed detailed error messages? | A05:2021 Security Misconfiguration |
| O04 | Which category recommends updating dependencies and removing unused components? | A06:2021 Vulnerable and Outdated Components |
| O05 | Which category recommends MFA and secure session management? | A07:2021 Identification and Authentication Failures |
| O06 | Which category covers insecure CI/CD pipelines and unverified software updates? | A08:2021 Software and Data Integrity Failures |
| O07 | Which category concerns missing audit logs and insufficient monitoring? | A09:2021 Security Logging and Monitoring Failures |
| O08 | Which category can expose internal APIs or cloud metadata through malicious URLs? | A10:2021 Server-Side Request Forgery |

## Negative and Unsupported Questions

The correct behavior is to say that the information is not available in the retrieved documents. The system must not invent an answer.

| ID | Question | Expected behavior |
|---|---|---|
| N01 | What is Devsinc's exact annual revenue? | State that the PDFs do not provide it |
| N02 | What is the monthly price of SkillPass? | State that pricing is not provided |
| N03 | Who is the CEO of VertXSoft? | State that the document does not identify a CEO |
| N04 | What was Systems Limited's closing share price yesterday? | State that current share-price data is not in the PDFs |
| N05 | What percentage of SkillPass users pass the official exam? | State that no pass-rate percentage is provided |
| N06 | What is the OWASP Top 10 list for 2025? | State that the available document covers the 2021 list |

## Manual Chunk-Quality Checklist

Inspect all stored chunks with `python view_db.py`. Mark each item pass or fail.

- [ ] No chunk contains only a heading.
- [ ] No chunk contains only one unfinished sentence.
- [ ] No chunk starts with continuation text such as "Over the years" without identifying its subject.
- [ ] A section heading remains with at least part of its explanation.
- [ ] List items remain with the correct heading.
- [ ] An OWASP category does not contain mitigation text belonging to another category.
- [ ] Company statistics remain associated with the correct company.
- [ ] SkillPass license names remain associated with their descriptions.
- [ ] Source metadata contains the correct `source_file`.
- [ ] Page metadata is preserved for every PDF chunk.
- [ ] Duplicate chunks are not stored after ingestion is run more than once.
- [ ] Very small chunks are reviewed manually.

## Current Baseline

The existing Chroma database contains 153 chunks:

| Source | Chunk count |
|---|---:|
| `Devsinc.pdf` | 30 |
| `OWASP top 10 vulnerabilities.pdf` | 36 |
| `Skill Pass.pdf` | 17 |
| `Systems Limited.pdf` | 34 |
| `vertxSoft.pdf` | 36 |

The current database includes chunks as short as 18-27 characters. Examples include incomplete continuation text such as `Over the years, the company`. These should be treated as chunk-quality failures even if retrieval sometimes returns the correct neighboring chunk.

## Test Result Template

Use this table to record results.

| Test ID | Top-1 source | Correct source in top 4? | Complete supporting context? | Answer accurate? | Pass/Fail | Notes |
|---|---|---|---|---|---|---|
| F01 |  |  |  |  |  |  |
| F02 |  |  |  |  |  |  |
| F03 |  |  |  |  |  |  |

## Overall Acceptance Target

- 100% pass on basic fact tests.
- At least 90% strong retrieval pass on paraphrase tests.
- 100% pass on company disambiguation tests.
- 100% refusal or "not available" behavior on unsupported questions.
- No incomplete chunks shorter than a meaningful sentence.
- No duplicate growth in Chroma after repeated ingestion.
