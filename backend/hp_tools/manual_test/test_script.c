#include <stdio.h>
#include <stdint.h>
#include "../hp_tools.h"

int main(void) {

  int current_temp = read_water_temperature();

  printf("current water temperature : %i\n", current_temp);
  printf("current target temperature : %i\n", (int) (read_target_water_temperature() / 10));

  const uint16_t target_temp = 24;
  int rc = set_target_water_temperature(target_temp);
  if (rc == -1) {
    printf("Error when trying to set the target water temperature\n");
    return -1;
  }


  printf("target temperature is now %i Celsius Degrees\n", (int) (read_target_water_temperature() / 10));

  return 0;
}
