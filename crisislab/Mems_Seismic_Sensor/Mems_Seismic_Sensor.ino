//#include <ArduinoJson.h>

//#include <SoftwareSerial.h>
#include "Protocentral_ADS1220.h"
#include <SPI.h>

#define PGA          1                 // Programmable Gain = 1
#define VREF         2.048            // Internal reference of 2.048V
#define VFSR         VREF/PGA
#define FULL_SCALE   (((long int)1<<23)-1)

#define ADS1220_CS_PIN    7
#define ADS1220_DRDY_PIN  A1

Protocentral_ADS1220 pc_ads1220;
int32_t adc_data;
volatile bool drdyIntrFlag = false;

void drdyInterruptHndlr(){
  drdyIntrFlag = true;
}

void enableInterruptPin(){

  attachInterrupt(digitalPinToInterrupt(ADS1220_DRDY_PIN), drdyInterruptHndlr, FALLING);
}
  


/*/
const unsigned long interval = 250; // Time interval in milliseconds
unsigned long previousMillis = 0;

const int bufferSize = 7; // Number of data points to collect
float bufferX[bufferSize];
float bufferY[bufferSize];
float bufferZ[bufferSize];
int bufferIndex = 0;


////////////////////SSID and password send/////////////////
int key = 0;
String w_SSID ;
String password ;


SoftwareSerial mySerial(3,2); // RX, TX pins

*/

void setup() {

  
  pinMode(ADS1220_CS_PIN, OUTPUT);
  pinMode(ADS1220_DRDY_PIN, INPUT_PULLUP);

//  Serial.begin(9600);
  Serial.begin(115200);
 // mySerial.begin(9600);
  
   pc_ads1220.begin(ADS1220_CS_PIN,ADS1220_DRDY_PIN);

    pc_ads1220.set_data_rate(DR_330SPS);
    pc_ads1220.set_pga_gain(PGA_GAIN_1);

    pc_ads1220.set_conv_mode_single_shot(); //Set Single shot mode
    
}

void loop() {

  unsigned long currentMillis = millis();
  // Convert milliseconds to seconds
  unsigned long seconds = currentMillis / 1000;

    float x = pc_ads1220.Read_SingleShot_SingleEnded_WaitForData(MUX_SE_CH2);
    Serial.print(convertToMilliV(x));
    Serial.print(","); 
    float y = pc_ads1220.Read_SingleShot_SingleEnded_WaitForData(MUX_SE_CH1);
    Serial.print(convertToMilliV(y));
    Serial.print(","); 
    float z = pc_ads1220.Read_SingleShot_SingleEnded_WaitForData(MUX_SE_CH0);
    Serial.println(convertToMilliV(z));
   Serial.println(currentMillis); 

 /* 
////////////////////SSID and password send/////////////////
  while (key < 1) {
    // Print a message to the serial monitor.
    Serial.println("Please enter the SSID:");

    while (Serial.available() < 1) {   }


    if (Serial.available() > 0) {
      // Read the text from the serial buffer.
      w_SSID = Serial.readStringUntil('\n');

      // Print the text to the console.
    //  Serial.print("SSID is:");
      Serial.println(w_SSID);
    }
    delay(1000);
  Serial.println("Please enter the Password:");
    while (Serial.available() < 1) {   }

     if (Serial.available() > 0) {
      // Read the text from the serial buffer.
      password = Serial.readStringUntil('\n');

      // Print the text to the console.
     // Serial.print("password is:");
      Serial.println(password);
      delay(1000);



///////////////////
 // Create a JSON object
  DynamicJsonDocument jsonDoc_login(256);

  // Add data to the JSON object
  jsonDoc_login["w_SSID"] = w_SSID;
  jsonDoc_login["password"] = password;

  // Serialize the JSON object into a string
  String jsonString_login;
  serializeJson(jsonDoc_login, jsonString_login);

  // Send the JSON string through serial communication

 for (int i = 1; i <= 15; i++) {
   mySerial.println(jsonString_login);
    Serial.println(jsonString_login);
    delay(1000);
  }
 

  delay(2000);  // Delay for 5 seconds before sending the next JSON object

//////////////////

      
    key = 2;
     }
  }
////////////////////SSID and password send/////////////////


if ( mySerial.available()) {
    String received_IP =  mySerial.readStringUntil('\n');
 Serial.println(received_IP);
}


//////////////////////////////////////////////////////

  unsigned long currentMillis = millis();

 // if (currentMillis - previousMillis >= interval) {
  //  previousMillis = currentMillis;

    // Collect accelerometer data for 250 milliseconds
    collectData();

    // Check if the buffer is full
    if (bufferIndex == bufferSize) {
      // Create a JSON object
      StaticJsonDocument<500> jsonDocument;

      // Populate the JSON object with stacked accelerometer data
      for (int i = 0; i < bufferSize; i++) {
        jsonDocument["x"][i] = bufferX[i];
        jsonDocument["y"][i] = bufferY[i];
        jsonDocument["z"][i] = bufferZ[i];
      }

      // Serialize the JSON object to a string
      String jsonString;
      serializeJson(jsonDocument, jsonString);

      // Send the JSON string through serial
      mySerial.println(jsonString);
      Serial.println(jsonString);

      // Reset buffer index
      bufferIndex = 0;
    }
  }
//}

void collectData() {
    float x = pc_ads1220.Read_SingleShot_SingleEnded_WaitForData(MUX_SE_CH2);
    float y = pc_ads1220.Read_SingleShot_SingleEnded_WaitForData(MUX_SE_CH1);
    float z = pc_ads1220.Read_SingleShot_SingleEnded_WaitForData(MUX_SE_CH0);

  // Stack accelerometer data to the buffers
  bufferX[bufferIndex] = x;
  bufferY[bufferIndex] = y;
  bufferZ[bufferIndex] = z;

  // Increment buffer index
  bufferIndex++;

  // Delay for 1 millisecond to avoid stacking duplicate values
  delay(2);
  */
}

float convertToMilliV(int32_t i32data)
{
    return (float)((i32data*VFSR*1000)/FULL_SCALE);
}
