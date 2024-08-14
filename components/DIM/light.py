import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import light, output, switch
from esphome.const import CONF_OUTPUT_ID

from ..PHCController import CONTROLLER_ID, PHCController

DEPENDENCIES = ["PHCController"]

ADDRESS = "dip"
CHANNEL = "channel"

dim_light_ns = cg.esphome_ns.namespace("DIM_light")
DIMLight = dim_light_ns.class_("DIM_light", cg.Component, light.LightOutput)

CONFIG_SCHEMA = cv.All(
    light.BRIGHTNESS_ONLY_LIGHT_SCHEMA.extend(
        {
            cv.GenerateID(CONF_OUTPUT_ID): cv.declare_id(DIMLight),
            cv.Required(CONTROLLER_ID): cv.use_id(PHCController),
            cv.Required(ADDRESS): cv.int_range(min=0, max=31),
            cv.Required(CHANNEL): cv.int_range(min=0, max=7),
            cv.Required(DIM_TIME): cv.All(
                cv.positive_time_period_milliseconds,
                cv.Range(
                    min=cv.TimePeriod(milliseconds=0),
                    max_included=cv.TimePeriod(milliseconds=655350),
                ),
            ),
        }
    ).extend(cv.COMPONENT_SCHEMA),
    _validate,
)


def to_code(config):
    controller = yield cg.get_variable(config[CONTROLLER_ID])
    var = cg.new_Pvariable(config[CONF_OUTPUT_ID])
    yield cg.register_component(var, config)
    yield light.register_light(var, config)

    cg.add(var.set_address(config[ADDRESS]))
    cg.add(var.set_channel(config[CHANNEL]))
    cg.add(var.set_dim_time(config[DIM_TIME]))

    cg.add(controller.register_AMD(var))
