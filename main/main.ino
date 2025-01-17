#include <Arduino.h>

#include "fuseegelee.h"
#include "trinketLed.h"

// Contains fuseeBin and FUSEE_BIN_SIZE
#include "hekate_ctcaer_5.0.2.h"

void setup() {
    ledInit();
    if (usbInit() == -1)
        sleepDeep(-1);

    while (!searchTegraDevice()) {
        ledBlink("orange", 1, 200);
    }

    setupTegraDevice();

    sendPayload(fuseeBin, FUSEE_BIN_SIZE, 0);

    launchPayload();

    sleepDeep(1);
}

void loop() {}
