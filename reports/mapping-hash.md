# Info

- **UTC date**: 2021-11-12 23:37:40.441161
- **Platform**: Windows-10-10.0.19043
- **Python version**: 3.9.8
- **Python compiler**: MSC v.1929 64 bit (AMD64)
- **Processor**: AMD64 Family 23 Model 24 Stepping 1, AuthenticAMD

# 10 items in dict

| Calculation way | Time required, s |
| :--- | ---: |
| `hash(frozenset(...))` | 0.662242000 |
| `Set._hash(...)` | 4.652880300 |
| Cached `Set._hash(...)` | 4.415362700 |

# 100 items in dict

| Calculation way | Time required, s |
| :--- | ---: |
| `hash(frozenset(...))` | 5.549967500 |
| `Set._hash(...)` | 34.928567600 |
| Cached `Set._hash(...)` | 36.285955600 |

# 1,000 items in dict

| Calculation way | Time required, s |
| :--- | ---: |
| `hash(frozenset(...))` | 51.531247300 |
| `Set._hash(...)` | 351.641779100 |
| Cached `Set._hash(...)` | 334.865616700 |

# 10,000 items in dict

| Calculation way | Time required, s |
| :--- | ---: |
| `hash(frozenset(...))` | 706.742159100 |
| `Set._hash(...)` | 3358.218408300 |
| Cached `Set._hash(...)` | 3500.571837500 |
