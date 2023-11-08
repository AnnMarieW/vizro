from __future__ import annotations

import itertools
from typing import List, Literal, Optional, cast

from dash import html
from pydantic import validator

from vizro.models import VizroBaseModel
from vizro.models._models_utils import _log_call
from vizro.models._navigation._navigation_utils import _validate_pages
from vizro.models._navigation.nav_item import NavItem
from vizro.models.types import NavPagesType


class NavBar(VizroBaseModel):
    """Navigation bar to be used as a selector for `Navigation`.

    Args:
        type (Literal["navbar"]): Defaults to `"navbar"`.
        pages (Optional[NavPagesType]): See [`NavPagesType`][vizro.models.types.NavPagesType].
            Defaults to `None`.
        items (List[NavItem]): See [`NavItem`][vizro.models.NavItem]. Defaults to `[]`.
    """

    type: Literal["navbar"] = "navbar"
    pages: Optional[NavPagesType] = None
    items: List[NavItem] = []

    # validators
    _validate_pages = validator("pages", allow_reuse=True, pre=True, always=True)(_validate_pages)

    @validator("items", always=True)
    def validate_items(cls, items, values):
        if not items:
            if isinstance(values.get("pages"), list):
                return [NavItem(pages=[page]) for page in values["pages"]]
            if isinstance(values.get("pages"), dict):
                return [NavItem(pages=value) for page, value in values["pages"].items()]

        return items

    @_log_call
    def build(self, active_page_id):
        return html.Div(
            children=[
                html.Div(
                    children=[item.build(active_page_id=active_page_id) for item in self.items],
                    className="nav-bar",
                    id="nav_bar_outer",
                ),
                self._nav_panel_build(active_page_id=active_page_id),
            ]
        )

    def _nav_panel_build(self, active_page_id):
        for item in self.items:
            pages = list(itertools.chain(*item.pages.values())) if isinstance(item.pages, dict) else item.pages
            if active_page_id in pages:
                return cast(NavBar, item.selector).build(active_page_id=active_page_id)

            return html.Div(hidden=True, id="nav_panel_outer")