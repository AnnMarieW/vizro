from __future__ import annotations

from typing import List, Optional

from dash import html
from pydantic import validator

from vizro.models import VizroBaseModel
from vizro.models._models_utils import _log_call
from vizro.models._navigation._navigation_utils import _validate_items
from vizro.models._navigation.nav_item import NavItem
from vizro.models._navigation.accordion import Accordion
from vizro.models.types import NavigationPagesType

class NavBar(VizroBaseModel):
    """NavBar to be used in Navigation Panel of Dashboard.

    Args:
        items (Optional[List[Icon]]): List of icons
    """

    pages: Optional[NavigationPagesType] = None
    items: Optional[List[NavItem]] = None

    # Re-used validators
    _validate_items = validator("items", allow_reuse=True, always=True)(_validate_items)

    @_log_call
    def pre_build(self):
        self._set_items()

    @_log_call
    def build(self, active_page_id):

        items = [item.build() for item in self.items]
        nav_bar = html.Div(
            children=items,
            className="nav_bar",
        )
        nav_panel = self._nav_panel_build(active_page_id=active_page_id)

        return nav_bar, nav_panel

    def _set_items(self):
        if not self.items:
            if isinstance(self.pages, list):
                self.items = [NavItem(pages=[page]) for page in self.pages]
            if isinstance(self.pages, dict):
                self.items = [NavItem(pages=value) for page, value in self.pages.items()]

            [item.pre_build() for item in self.items]

    def _nav_panel_build(self, active_page_id):
        for item in self.items:
            if isinstance(item.pages, list):
                if active_page_id in item.pages:
                    return item._selector.build(active_page_id=active_page_id)

            if isinstance(item.pages, dict):
                pages = [page for row in item.pages.values() for page in row]
                if active_page_id in pages:
                    return item._selector.build(active_page_id=active_page_id)
