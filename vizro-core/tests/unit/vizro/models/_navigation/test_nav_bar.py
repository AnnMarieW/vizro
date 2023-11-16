"""Unit tests for vizro.models.NavBar."""
import json
import re

import plotly
import pytest
from dash import html
from pydantic import ValidationError

import vizro.models as vm


@pytest.mark.usefixtures("vizro_app", "prebuilt_dashboard")
class TestNavBarInstantiation:
    """Tests NavBar model instantiation."""

    def test_navbar_mandatory_only(self):
        nav_bar = vm.NavBar()

        assert hasattr(nav_bar, "id")
        assert nav_bar.pages == {}
        assert nav_bar.items == []

    def test_navbar_mandatory_and_optional(self, pages_as_dict):
        nav_item = vm.NavItem(text="Text")
        nav_bar = vm.NavBar(id="nav_bar", pages=pages_as_dict, items=[nav_item])

        assert nav_bar.id == "nav_bar"
        assert nav_bar.pages == pages_as_dict
        assert nav_bar.items == [nav_item]

    def test_valid_pages_as_list(self, pages_as_list):
        nav_bar = vm.NavBar(pages=pages_as_list)
        assert nav_bar.pages == {"Page 1": ["Page 1"], "Page 2": ["Page 2"]}

    @pytest.mark.parametrize("pages", [{"Group": []}, []])
    def test_invalid_field_pages_no_ids_provided(self, pages):
        with pytest.raises(ValidationError, match="Ensure this value has at least 1 item."):
            vm.NavBar(pages=pages)

    def test_invalid_field_pages_wrong_input_type(self):
        with pytest.raises(ValidationError, match="unhashable type: 'Page'"):
            vm.NavBar(pages=[vm.Page(title="Page 3", components=[vm.Button()])])

    @pytest.mark.parametrize("pages", [["non existent page"], {"Group": ["non existent page"]}])
    def test_invalid_page(self, pages):
        with pytest.raises(
            ValidationError, match=re.escape("Unknown page ID ['non existent page'] provided to " "argument 'pages'.")
        ):
            vm.NavBar(pages=pages)


@pytest.mark.usefixtures("vizro_app", "prebuilt_dashboard")
class TestNavBarPreBuildMethod:
    def test_default_items(self, pages_as_dict):
        nav_bar = vm.NavBar(pages=pages_as_dict)
        nav_bar.pre_build()
        assert all(isinstance(item, vm.NavItem) for item in nav_bar.items)
        assert all(item.icon == f"filter_{position}" for position, item in enumerate(nav_bar.items, 1))

    def test_items_with_with_pages_icons(self, pages_as_dict):
        nav_items = [
            vm.NavItem(text="Text", pages={"Group 1": ["Page 1"]}, icon="Home"),
            vm.NavItem(text="Text", pages={"Group 2": ["Page 2"]}),
        ]
        nav_bar = vm.NavBar(pages=pages_as_dict, items=nav_items)
        nav_bar.pre_build()
        assert nav_bar.items == nav_items
        assert nav_bar.items[0].icon == "Home"
        assert nav_bar.items[1].icon == "filter_2"


@pytest.mark.usefixtures("vizro_app", "prebuilt_dashboard")
class TestNavBarBuildMethod:
    """Tests NavBar model build method."""

    def test_nav_bar_active(self, pages_as_dict):
        nav_bar = vm.NavBar(pages=pages_as_dict)
        nav_bar.pre_build()
        built_nav_bar = nav_bar.build(active_page_id="Page 1")
        assert isinstance(built_nav_bar["nav_bar_outer"], html.Div)
        assert isinstance(built_nav_bar["nav_panel_outer"], html.Div)
        assert not hasattr(built_nav_bar["nav_panel_outer"], "hidden")

    def test_nav_bar_not_active(self, pages_as_dict):
        nav_bar = vm.NavBar(pages=pages_as_dict)
        nav_bar.pre_build()
        built_nav_bar = nav_bar.build(active_page_id="Page 3")
        assert isinstance(built_nav_bar["nav_bar_outer"], html.Div)
        assert isinstance(built_nav_bar["nav_panel_outer"], html.Div)
        assert built_nav_bar["nav_panel_outer"].hidden
