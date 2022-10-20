/**
 * @file time_core.h
 * @author Jasper Di Francesco (jasper.difrancesco@gmail.com)
 * @brief Header file for time_core.c, RTC functionality for the imx8mm board
 * @version 0.1
 * @date 2022-10-20
 * 
 * @copyright Copyright (c) 2022
 * 
 */

#pragma once

int rtc_enable(void);

void rtc_stat(void);

uint64_t rtc_now(void);
uint64_t rtc_now_ms(void);