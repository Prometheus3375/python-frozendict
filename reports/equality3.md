# Info

- **UTC date**: 2022-11-13 20:34:06.643442
- **Platform**: Windows-10-10.0.19044-SP0
- **Python version**: 3.9.13
- **Python compiler**: MSC v.1929 64 bit (AMD64)
- **Processor**: AMD64 Family 23 Model 24 Stepping 1, AuthenticAMD

# 10 items in dictionaries

## frozendict == 1

| Implementation | Time required, s | Relative to `FrozendictBase1` |
| :--- | ---: | ---: |
| `FrozendictBase1` | 0.423413600 | - |
| `FrozendictBase2` | 0.139083400 | 32.85% |
| `FrozendictBase3` | 0.139999800 | 33.06% |

## frozendict == 'value'

| Implementation | Time required, s | Relative to `FrozendictBase1` |
| :--- | ---: | ---: |
| `FrozendictBase1` | 0.437472200 | - |
| `FrozendictBase2` | 0.135268600 | 30.92% |
| `FrozendictBase3` | 0.134962400 | 30.85% |

## frozendict == dict

| Implementation | Time required, s | Relative to `FrozendictBase1` |
| :--- | ---: | ---: |
| `FrozendictBase1` | 0.462172500 | - |
| `FrozendictBase2` | 0.149108100 | 32.26% |
| `FrozendictBase3` | 0.171621800 | 37.13% |

## frozendict == frozendict

| Implementation | Time required, s | Relative to `FrozendictBase1` |
| :--- | ---: | ---: |
| `FrozendictBase1` | 0.350239200 | - |
| `FrozendictBase2` | 0.433863400 | 123.88% |
| `FrozendictBase3` | 0.406306700 | 116.01% |

## frozendict == other_frozendict

| Implementation | Time required, s | Relative to `FrozendictBase1` |
| :--- | ---: | ---: |
| `FrozendictBase1` | 0.262179600 | - |
| `FrozendictBase2` | 0.293041200 | 111.77% |
| `FrozendictBase3` | 0.241315200 | 92.04% |

# 100 items in dictionaries

## frozendict == 1

| Implementation | Time required, s | Relative to `FrozendictBase1` |
| :--- | ---: | ---: |
| `FrozendictBase1` | 0.477530200 | - |
| `FrozendictBase2` | 0.146662400 | 30.71% |
| `FrozendictBase3` | 0.147740700 | 30.94% |

## frozendict == 'value'

| Implementation | Time required, s | Relative to `FrozendictBase1` |
| :--- | ---: | ---: |
| `FrozendictBase1` | 0.502799700 | - |
| `FrozendictBase2` | 0.133812600 | 26.61% |
| `FrozendictBase3` | 0.143547900 | 28.55% |

## frozendict == dict

| Implementation | Time required, s | Relative to `FrozendictBase1` |
| :--- | ---: | ---: |
| `FrozendictBase1` | 0.557727200 | - |
| `FrozendictBase2` | 0.192929000 | 34.59% |
| `FrozendictBase3` | 0.165184000 | 29.62% |

## frozendict == frozendict

| Implementation | Time required, s | Relative to `FrozendictBase1` |
| :--- | ---: | ---: |
| `FrozendictBase1` | 2.135278500 | - |
| `FrozendictBase2` | 2.424310300 | 113.54% |
| `FrozendictBase3` | 2.057726000 | 96.37% |

## frozendict == other_frozendict

| Implementation | Time required, s | Relative to `FrozendictBase1` |
| :--- | ---: | ---: |
| `FrozendictBase1` | 0.264716700 | - |
| `FrozendictBase2` | 0.224475300 | 84.80% |
| `FrozendictBase3` | 0.306828900 | 115.91% |

# 1,000 items in dictionaries

## frozendict == 1

| Implementation | Time required, s | Relative to `FrozendictBase1` |
| :--- | ---: | ---: |
| `FrozendictBase1` | 0.568691200 | - |
| `FrozendictBase2` | 0.156094400 | 27.45% |
| `FrozendictBase3` | 0.160204500 | 28.17% |

## frozendict == 'value'

| Implementation | Time required, s | Relative to `FrozendictBase1` |
| :--- | ---: | ---: |
| `FrozendictBase1` | 0.528119300 | - |
| `FrozendictBase2` | 0.141730200 | 26.84% |
| `FrozendictBase3` | 0.154372200 | 29.23% |

## frozendict == dict

| Implementation | Time required, s | Relative to `FrozendictBase1` |
| :--- | ---: | ---: |
| `FrozendictBase1` | 0.587199400 | - |
| `FrozendictBase2` | 0.183260500 | 31.21% |
| `FrozendictBase3` | 0.185320200 | 31.56% |

## frozendict == frozendict

| Implementation | Time required, s | Relative to `FrozendictBase1` |
| :--- | ---: | ---: |
| `FrozendictBase1` | 21.337945900 | - |
| `FrozendictBase2` | 20.026820500 | 93.86% |
| `FrozendictBase3` | 20.108475300 | 94.24% |

## frozendict == other_frozendict

| Implementation | Time required, s | Relative to `FrozendictBase1` |
| :--- | ---: | ---: |
| `FrozendictBase1` | 0.252416100 | - |
| `FrozendictBase2` | 0.222726200 | 88.24% |
| `FrozendictBase3` | 0.276425200 | 109.51% |

