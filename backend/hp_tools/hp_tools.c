#include <stdio.h>
#include <errno.h>
#include <stdint.h>
#include <stdlib.h>
#include <inttypes.h>
#include <modbus.h>
#include "hp_tools.h"

char *device = "/dev/ttyUSB0";
int baud_rate = 9600;
char parity = 'E';
int data_bits = 8;
int stop_bits = 1;
int heating_pump_id = 9;

int rc;


modbus_t *create_modbus_ctx_and_connect() {
  // create a modbus RTU context with the correct parameters
  modbus_t *ctx = modbus_new_rtu(device, baud_rate, parity, data_bits, stop_bits);

  if (ctx == NULL) {
    // handle errors
    fprintf(stderr, "Unable to create the libmodbus context\n");
    return NULL;
  }

  // set the slave id of the heating pump
  rc = modbus_set_slave(ctx, heating_pump_id);

  if (rc == -1) {
    // handle errors
      fprintf(stderr, "Invalid slave ID\n");
      modbus_free(ctx);
      return NULL;
  }

  // try to establish the connection, else returns an error
  if (modbus_connect(ctx) == -1) {
      fprintf(stderr, "Connection failed: %s\n", modbus_strerror(errno));
      modbus_free(ctx);
      return NULL;
  }

  return ctx;
}



// read the temperature of the water from the water temperature probe
// params : None
// returns : int
int read_water_temperature() {
  modbus_t *ctx = create_modbus_ctx_and_connect();
  if (ctx == NULL) {
    fprintf(stderr, "Error when trying to create a modbus context and connect to the device. See previous errors.\n");
    return -1;
  }

  // allocate 16 bits to retrieve the integer corresponding to the temperature
  uint16_t *water_temperature;
  water_temperature = (uint16_t *) malloc(sizeof(uint16_t));
  if (water_temperature == NULL) {
    return -1;
  }

  // read the water temperature register
  rc = modbus_read_input_registers(ctx, 8, 1, water_temperature);
  if (rc == -1) {
      fprintf(stderr, "%s\n", modbus_strerror(errno));
      return -1;
  }

  int output = *water_temperature;

  // free the 16 bits for the temperature
  free(water_temperature);

  // close the modbus connection and free the context
  modbus_close(ctx);
  modbus_free(ctx);

  return output;
}


// read the target temperature of the water
// returns : int : the target water temperature in tenth of cesius degrees
int read_target_water_temperature() {
  modbus_t *ctx = create_modbus_ctx_and_connect();
  if (ctx == NULL) {
    fprintf(stderr, "Error when trying to create a modbus context and connect to the device. See previous errors.\n");
    return -1;
  }

  // allocate 16 bits to retrieve the integer corresponding to the target temperature
  uint16_t *target_temperature;
  target_temperature = (uint16_t *) malloc(sizeof(uint16_t));
  if (target_temperature == NULL) {
    return -1;
  }

  // read the target water temperature register
  rc = modbus_read_registers(ctx, 36, 1, target_temperature);
  if (rc == -1) {
      fprintf(stderr, "%s\n", modbus_strerror(errno));
      return -1;
  }

  int output = *target_temperature;

  // free the 16 bits for the target temperature
  free(target_temperature);

  // close the modbus connection and free the context
  modbus_close(ctx);
  modbus_free(ctx);

  return output;
}


// set the target temperature of the water
// params : int target_temp : the target water temperature in cesius degrees
// returns : int
int set_target_water_temperature(int target_temp) {
  modbus_t *ctx = create_modbus_ctx_and_connect();
  if (ctx == NULL) {
    fprintf(stderr, "Error when trying to create a modbus context and connect to the device. See previous errors.\n");
    return -1;
  }


  // write in the target water temperature register
  rc = modbus_write_register(ctx, 36, 10 * target_temp);
  if (rc == -1) {
      fprintf(stderr, "%s\n", modbus_strerror(errno));
      return -1;
  }

  // close the modbus connection and free the context
  modbus_close(ctx);
  modbus_free(ctx);

  return target_temp;
}
