import re

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CURRENCY_RUB
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([VoxnetBalanceSensor(coordinator, entry.entry_id)])


class VoxnetBalanceSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Баланс интернета"
    _attr_native_unit_of_measurement = CURRENCY_RUB
    _attr_icon = "mdi:wallet-outline"
    _attr_suggested_display_precision = 2

    def __init__(self, coordinator, entry_id: str):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_internet_balance"

    @property
    def native_value(self):
        if not self.coordinator.data:
            return None

        raw = self.coordinator.data.get("Баланс") or self.coordinator.data.get("Р‘Р°Р»Р°РЅСЃ")
        if not raw:
            return None

        normalized = raw.replace("\xa0", " ").replace(",", ".")
        match = re.search(r"-?\d+(?:\.\d+)?", normalized)
        if not match:
            return None

        return float(match.group(0))

    @property
    def extra_state_attributes(self):
        return self.coordinator.data
