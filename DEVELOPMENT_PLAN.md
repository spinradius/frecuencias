# Development Plan: Streamlit Frequency Spectrum Analyzer

## 1. Current State Analysis
- **Core Functionality**: Visualizes frequency spectrum data for multiple instruments using Plotly bar charts in Streamlit.
- **Recent Optimizations**: 
  - Vectorized Plotly traces (15 bars → 1 trace).
  - `lru_cache` for frequency-to-Y mapping.
  - Pre-computed layout columns.
- **Tech Stack**: Python, Streamlit, Plotly, Pandas, NumPy.

## 2. Proposed Improvements

### Phase 1: Performance & Scalability (High Priority)
- [ ] **Data Streaming**: Implement `st.cache_data` with TTL for real-time data sources to prevent stale data without full re-runs.
- [ ] **Downsampling**: Add logic to automatically downsample data if the instrument count exceeds a threshold (e.g., >50 instruments) to maintain FPS.
- [ ] **WebAssembly/Pyodide**: Explore offloading heavy frequency calculations to the client side if the dataset grows massive.

### Phase 2: User Experience & Interactivity (Medium Priority)
- [ ] **Instrument Filtering**: Add a multi-select sidebar widget to toggle visibility of specific instruments without reloading data.
- [ ] **Dynamic Thresholding**: Allow users to set a dB threshold slider to hide low-amplitude noise visually.
- [ ] **Export Features**: Add buttons to download the current view as PNG/SVG or export the filtered data as CSV.
- [ ] **Responsive Layout**: Ensure the chart scales correctly on mobile devices using Streamlit's container options.

### Phase 3: Code Quality & Maintainability (Medium Priority)
- [ ] **Type Hinting**: Add full Python type hints to `freq_to_y` and data processing functions.
- [ ] **Unit Tests**: Create `pytest` suite for data transformation logic and edge cases (e.g., empty input, invalid frequencies).
- [ ] **Configuration Management**: Move hardcoded constants (colors, frequency ranges) to a `config.yaml` or `.env` file.
- [ ] **Logging**: Replace `print` statements with the `logging` module for better debugging in production.

### Phase 4: Advanced Features (Low Priority / Future)
- [ ] **Heatmap Mode**: Offer an alternative "Waterfall" view (Frequency vs. Time vs. Intensity) for historical analysis.
- [ ] **Annotation System**: Allow users to click and label specific peaks directly on the chart.
- [ ] **Multi-Page App**: Split "Live View", "Historical Data", and "Settings" into separate Streamlit pages.

## 3. Implementation Roadmap

| Step | Task | Estimated Effort | Dependencies |
| :--- | :--- | :--- | :--- |
| 1 | Add Sidebar Filters & Export Buttons | 2 hours | None |
| 2 | Implement Unit Tests & Type Hinting | 3 hours | None |
| 3 | Optimize for Large Datasets (Downsampling) | 4 hours | Step 1 |
| 4 | Refactor Config & Logging | 2 hours | None |
| 5 | Develop Heatmap Visualization | 6 hours | Step 3 |

## 4. Immediate Next Steps
1. **Initialize Testing Environment**: Set up `pytest` and write the first test case for `freq_to_y`.
2. **UI Enhancement**: Implement the instrument multi-select filter in `reg.py`.
3. **Documentation**: Add docstrings to all public functions and a `README.md` with usage instructions.
