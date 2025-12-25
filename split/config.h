// Copyright 2022 Yoichiro Tanaka (@yoichiro)
// SPDX-License-Identifier: GPL-2.0-or-later

#pragma once

// прошивка двойным нажатием на сброс https://docs.qmk.fm/platformdev_rp2040#double-tap
#define RP2040_BOOTLOADER_DOUBLE_TAP_RESET
#define RP2040_BOOTLOADER_DOUBLE_TAP_RESET_LED GP25
#define RP2040_BOOTLOADER_DOUBLE_TAP_RESET_TIMEOUT 500U

#define SERIAL_USART_FULL_DUPLEX
#define SERIAL_USART_TX_PIN GP0
#define SERIAL_USART_RX_PIN GP1

//#define SERIAL_DEBUG

#define WS2812_PIO_USE_PIO1

/*
 * Feature disable options
 *  These options are also useful to firmware size reduction.
 */

/* disable debug print */
//#define NO_DEBUG

/* disable print */
//#define NO_PRINT

/* disable action features */
//#define NO_ACTION_LAYER
//#define NO_ACTION_TAPPING
//#define NO_ACTION_ONESHOT

// значения по умолчанию для oled:
// #define I2C_DRIVER I2CD1
// #define I2C1_SDA_PIN GP2
// #define I2C1_SCL_PIN GP3

#define OLED_BRIGHTNESS 64
#define I2C_DRIVER I2CD0
#define I2C1_SDA_PIN GP4
#define I2C1_SCL_PIN GP5
#define OLED_DISPLAY_128X64

#define DEBUG_MATRIX_SCAN_RATE
