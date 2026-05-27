#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// ================= LCD =================
LiquidCrystal_I2C lcd(0x27, 16, 2);

// ================= PINS =================
int occupyBtn = 2;
int freeBtn   = 3;

int redLED    = 8;
int greenLED  = 9;

int buzzer    = 10;

// ================= VARIABLES =================
unsigned long startTime = 0;

unsigned long lastFreeTime = 0;

unsigned long idleTime = 0;

bool sessionActive = false;

int customerCount = 0;

// ================= NOTES =================
int C  = 262;
int E  = 330;
int G  = 392;
int C2 = 523;

// ===================================================
// FUNCTION : PLAY NOTE
// ===================================================
void playNote(int freq, int duration) {

  tone(buzzer, freq);

  delay(duration);

  noTone(buzzer);

  delay(70);
}

// ===================================================
// OCCUPIED SOUND
// ===================================================
void occupySound() {

  tone(buzzer, 220);
  delay(300);

  noTone(buzzer);
  delay(80);

  tone(buzzer, 262);
  delay(350);

  noTone(buzzer);
}

// ===================================================
// FREE SOUND
// ===================================================
void freeSound() {

  playNote(C, 350);

  playNote(E, 350);

  playNote(G, 500);

  playNote(C2, 650);
}

// ===================================================
// SETUP
// ===================================================
void setup() {

  Serial.begin(9600);

  // Buttons
  pinMode(occupyBtn, INPUT_PULLUP);
  pinMode(freeBtn, INPUT_PULLUP);

  // LEDs
  pinMode(redLED, OUTPUT);
  pinMode(greenLED, OUTPUT);

  // Buzzer
  pinMode(buzzer, OUTPUT);

  // LCD
  lcd.init();
  lcd.backlight();

  // Startup Screen
  lcd.setCursor(0, 0);
  lcd.print("SMART COUNTER");

  lcd.setCursor(0, 1);
  lcd.print("System Ready");

  delay(2000);

  lcd.clear();

  // Default State
  digitalWrite(greenLED, HIGH);
  digitalWrite(redLED, LOW);

  lcd.setCursor(0, 0);
  lcd.print("Counter Free");

  lcd.setCursor(0, 1);
  lcd.print("Ready Next");

  // Initialize free time
  lastFreeTime = millis();
}

// ===================================================
// LOOP
// ===================================================
void loop() {

  // ==========================================
  // OCCUPY BUTTON
  // ==========================================
  if (digitalRead(occupyBtn) == LOW &&
      sessionActive == false) {

    sessionActive = true;

    customerCount++;

    startTime = millis();

    // Calculate idle time
    idleTime =
      (startTime - lastFreeTime) / 1000;

    // LEDs
    digitalWrite(redLED, HIGH);
    digitalWrite(greenLED, LOW);

    // LCD
    lcd.clear();

    lcd.setCursor(0, 0);
    lcd.print("Counter Busy");

    lcd.setCursor(0, 1);
    lcd.print("Serving #");
    lcd.print(customerCount);

    // Serial Live Status
    Serial.println("BUSY");

    // Sound
    occupySound();

    delay(300);
  }

  // ==========================================
  // FREE BUTTON
  // ==========================================
  if (digitalRead(freeBtn) == LOW &&
      sessionActive == true) {

    sessionActive = false;

    // LEDs
    digitalWrite(redLED, LOW);
    digitalWrite(greenLED, HIGH);

    // Timing
    unsigned long endTime = millis();

    unsigned long duration =
      (endTime - startTime) / 1000;

    // Save free timestamp
    lastFreeTime = endTime;

    // LCD
    lcd.clear();

    lcd.setCursor(0, 0);
    lcd.print("Counter Free");

    lcd.setCursor(0, 1);
    lcd.print("Time:");
    lcd.print(duration);
    lcd.print(" sec");

    // Serial Live Status
    Serial.println("FREE");

    // ==================================
    // LOGGER FORMAT
    // ==================================
    Serial.print("LOG,");

    Serial.print(customerCount);

    Serial.print(",");

    Serial.print(duration);

    Serial.print(",");

    Serial.println(idleTime);

    // Sound
    freeSound();

    delay(2500);

    // Reset LCD
    lcd.clear();

    lcd.setCursor(0, 0);
    lcd.print("Counter Free");

    lcd.setCursor(0, 1);
    lcd.print("Ready Next");

    delay(300);
  }
}