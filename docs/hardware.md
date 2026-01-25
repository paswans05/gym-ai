# Hardware Compatibility Guide for GymAI

To switch from "Mock Mode" to real-time CSI capture, you need specific hardware that supports Channel State Information (CSI) extraction. Standard home routers usually lock this feature.

## Recommended Option: ESP32 (Easiest & Cheapest)
For a home gym setup, the **ESP32** microcontroller is the best choice.
-   **Cost**: ~$5 - $10 USD per board.
-   **Requirements**: Two ESP32 development boards (one transmitter, one receiver).
-   **Software**: [esp32-csi-tool](https://github.com/stevenmhernandez/esp32-csi-tool).
-   **Pros**: Cheap, small, low power, easy to program via USB.

## Router Shopping List (Buy One of These)
If you insist on using a router, you **MUST** replace your current ISP router with one of these specific models. Your ZTE/RichLink routers **will not work**.

| Brand | Model | Version | Notes |
| :--- | :--- | :--- | :--- |
| **TP-Link** | **Archer C7** | **v2** | Highly Recommended. Uses Atheros QCA9558. Widely used in research. |
| **TP-Link** | **TL-WR1043ND** | **v2, v3, v4** | Very cheap, finding specific versions can be hard. |
| **Asus** | **RT-AC86U** | Any | Supports Nexmon (Wi-Fi 5). More expensive but powerful. |
| **Raspberry Pi** | **4 Model B** | Any | Not a router, but acts like one for this purpose. Easier to setup than old routers. |

> [!WARNING]
> You must get the **EXACT Hardware Version** listed above. For example, Archer C7 **v5** DOES NOT WORK. Only **v2** works.

## Known Unsupported Devices
These devices have been checked and are **confirmed to NOT work**:
- **RichLink RL841GWV-DGB** (Locked firmware, unsupported chipset).
- **ZTE ZXHN F670L** (GPON ONT, locked firmware).
- **Laptop Wi-Fi (Windows)**: Your **Killer AX1650i** (Intel AX200) is **unsupported on Windows**. It requires complex Linux setup.

## Research Standard (Laptop Required)
**Intel 5300 NIC**
-   Requires a laptop with a Mini-PCIe slot (or an adapter).
-   The "Gold Standard" for academic research.
-   **Linux 802.11n CSI Tool** (Halperin et al.).

## Summary
1.  **Get two ESP32 boards** if you want to get started quickly and cheaply.
2.  **Use a Raspberry Pi 4** if you already have one and are comfortable with patching kernel firmware (Nexmon).
