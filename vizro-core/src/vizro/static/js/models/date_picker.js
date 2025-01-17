function update_date_picker_values(value, input_store) {
  if (Array.isArray(value) && value[1] === null) {
    if (value[0] !== null) {
      // The user starts selecting a range
      // For example: value=["2025-01-01", null]
      // No updates to the value or input store.
      // Ideally, this date_picker should not be triggered in after date_picker selection is finished.
      return dash_clientside.no_update;
    }
    if (value[0] === null) {
      // The user started selecting a range and then unfocused the date_picker by clicking somewhere else
      // value=[null, null]
      // Update the date_picker value with the previous value from input store
      return [input_store, dash_clientside.no_update];
    }
  }

  // date_picker is properly selected
  // For example: value=["2025-01-01", "2025-01-02"]
  // Update the input store
  return [dash_clientside.no_update, value];
}

window.dash_clientside = {
  ...window.dash_clientside,
  date_picker: {
    update_date_picker_values: update_date_picker_values,
  },
};
