"""Support for HomeWizard buttons."""
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import HWEnergyDeviceUpdateCoordinator
from .entity import HomeWizardEntity
from .helpers import homewizard_exception_handler


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Identify button."""
    coordinator: HWEnergyDeviceUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    if coordinator.data.features.has_identify:
        async_add_entities([HomeWizardIdentifyButton(coordinator, entry)])


class HomeWizardIdentifyButton(HomeWizardEntity, ButtonEntity):
    """Representation of a identify button."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:magnify"
    _attr_name = "Identify"

    def __init__(
        self,
        coordinator: HWEnergyDeviceUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize button."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.unique_id}_identify"

    @homewizard_exception_handler
    async def async_press(self) -> None:
        """Identify the device."""
        await self.coordinator.api.identify()
