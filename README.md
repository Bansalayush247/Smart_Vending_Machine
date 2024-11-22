# Smart Vending Machine  

**A seamless and modern vending experience powered by NFC, NodeMCU, and Raspberry Pi**  

---

## **Overview**  

The **Smart Vending Machine** project modernizes traditional vending systems by enabling contactless interaction. Users can scan their NFC-enabled devices, browse items through a dynamic web interface, and complete purchases with ease. This innovative approach enhances hygiene, convenience, and operational efficiency.  

---

## **Work Flow**

![image](https://github.com/user-attachments/assets/4f4cb40a-4db1-4070-82b5-fd587d18440b)

---

## **Features**  

- **Dynamic NFC Integration**: Identifies users via NFC-enabled devices using NodeMCU and an RFID scanner.  
- **User-Friendly Web Interface**: Grid-based layout for simplified product browsing and easy purchases.  
- **Error Handling**: Comprehensive error handling for all API interactions ensures smooth user experiences.  
- **Asynchronous UI Updates**: Non-blocking, real-time interface updates for seamless operation.  
- **Efficient DOM Manipulation**: Uses map-reduce techniques for optimal performance.  

---

## **Technologies Used**  

- **Hardware**:  
  - NodeMCU Microcontroller  
  - RFID Scanner  
  - Raspberry Pi 3  

- **Software**:  
  - Backend Application on Raspberry Pi  
  - NFC Integration via NodeMCU  
  - Dynamic Web Application  

---

## **Project Workflow**  

1. **Scan**: Users scan their NFC-enabled devices (phones) via the RFID scanner.  
2. **Identify**: NodeMCU processes the scanned data and forwards it to Raspberry Pi.  
3. **Browse**: Raspberry Pi hosts a web interface, enabling users to browse and select products.  
4. **Purchase**: Users complete transactions via the web application for a seamless, contactless experience.  

---

## **Analysis and Findings**  

- **Initial Challenges**:  
  - MQTT was explored for communication but was incompatible with hardware, leading to the adoption of HTTP.  
  - Using Raspberry Pi on both ends was deemed redundant.  

- **Solutions**:  
  - NodeMCU proved to be the ideal intermediary between the RFID reader and Raspberry Pi.  

---

## **Future Enhancements**  

1. **Adopt BLE (Bluetooth Low Energy)** for short-range, energy-efficient data exchange.  
2. **Implement LoRaWAN** for low-power, long-range communication in remote deployments.  
3. **Revisit MQTT** using advanced microcontrollers like ESP32 for better message brokering.  
4. **Hybrid Protocols**: Combine HTTP, WebSockets, and BLE for versatile communication.  
5. **Edge Computing**: Enable localized decision-making to reduce server dependency.  

---

## **How to Use**  

1. **Setup Hardware**:  
   - Connect the NodeMCU with an RFID scanner.  
   - Link the Raspberry Pi to host the backend and web application.  

2. **Run Backend Application**:  
   - Deploy the web interface on Raspberry Pi.  
   - Ensure NodeMCU and Raspberry Pi are networked.  

3. **Interact**:  
   - Users scan their NFC-enabled devices to browse and purchase items seamlessly.  

---

## **Contributors**  

Developed by [Ayush Bansal](https://github.com/bansalayush247), [Devarsh Parmar](https://github.com/DEVMYTH123).  

---  

Feel free to contribute, open issues, or share feedback! 🚀  
