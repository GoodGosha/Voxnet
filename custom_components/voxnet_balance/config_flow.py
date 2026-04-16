import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN


class VoxnetConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input:
            await self.async_set_unique_id(user_input["username"])
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title="Voxnet",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("username"): str,
                    vol.Required("password"): str,
                }
            ),
        )
