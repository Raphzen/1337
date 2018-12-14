#include <stdio.h>

#define BLYNK_PRINT Serial
#include <SPI.h>
#include <Ethernet.h>
#include <BlynkSimpleEthernet.h>

int main() {
    Blynk();
}

int Blynk(){
    Blynk.begin();

    BLYNK_AUTH="e9923f06747e4e44a698f04324c909ec"

    BLYNK_WRITE(V0){
        int r=param.asInt();
        printf(r"\n");
    }
}