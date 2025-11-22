# Architecture Documentation

## Overview

PDF Table Title Fixer is built with a modular, scalable architecture that separates concerns and allows for easy extension with additional APA rules.

## Architecture Principles

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Scalability**: Easy to add new APA rules without modifying existing code
3. **Type Safety**: Uses dataclasses and type hints throughout
4. **Error Handling**: Custom exceptions for better error management
5. **Testability**: Modular design facilitates unit testing

## Module Structure

### Core Module (`src/core/`)

Business logic for PDF analysis and modification.

#### `models.py`
Data models using Python dataclasses:
- `TableInfo`: Information about detected tables
- `FormatInfo`: Font and formatting information
- `Modification`: Represents a modification to apply
- `AnalysisResult`: Complete analysis result

#### `analyzer.py`
PDF analysis functionality:
- `PDFAnalyzer`: Detects tables in PDF files
- Methods for finding consecutive repetitions
- Grouping tables by number

#### `formatter.py`
Format detection and analysis:
- `FormatAnalyzer`: Extracts format information from PDF
- Checks format uniformity
- Gets common format from multiple samples

#### `modifier.py`
PDF modification functionality:
- `PDFModifier`: Applies modifications to PDF files
- Text replacement with format preservation
- Font mapping and fallback handling

### Rules Module (`src/rules/`)

Scalable rule system for APA compliance.

#### `base_rule.py`
Abstract base class for all APA rules:
- `analyze()`: Analyze PDF for rule violations
- `apply()`: Apply rule modifications
- `validate()`: Validate modifications

#### `table_title_rule.py`
Implementation of table title numbering rule:
- Inherits from `BaseRule`
- Uses core modules for analysis and modification
- Handles format detection and uniformity

#### `future_rules/`
Directory for future APA rule implementations:
- Citation rules
- Reference formatting rules
- Other APA compliance rules

### GUI Module (`src/gui/`)

User interface components.

#### `main_window.py`
Main application window:
- Integrates all components
- Handles user interactions
- Manages application state

#### `components/`
Reusable GUI components:
- `file_selector.py`: PDF file selection
- `results_panel.py`: Analysis results display
- `format_controls.py`: Format customization

#### `themes/`
Theme and styling:
- `fluent_theme.py`: Fluent Design color palette and styles

### Utils Module (`src/utils/`)

Utility functions and helpers.

#### `validators.py`
Input validation:
- PDF path validation
- File size checks
- Format parameter validation

#### `exceptions.py`
Custom exceptions:
- `PDFProcessingError`: Base exception
- `PDFReadError`: PDF reading errors
- `FormatDetectionError`: Format detection errors
- `ModificationError`: Modification errors
- `ValidationError`: Validation errors

#### `constants.py`
Application constants:
- Regex patterns
- Default values
- UI constants

## Data Flow

1. **File Selection**: User selects PDF file
2. **Analysis**: `TableTitleRule.analyze()` is called
   - `PDFAnalyzer` detects all tables
   - `FormatAnalyzer` extracts format information
   - Results are structured as `AnalysisResult`
3. **Display**: Results are shown in GUI components
4. **User Configuration**: User configures format options
5. **Modification**: `TableTitleRule.apply()` is called
   - `PDFModifier` applies changes to PDF
   - Modified PDF is saved

## Extending the System

### Adding a New APA Rule

1. Create a new file in `src/rules/` (or `src/rules/future_rules/`)
2. Inherit from `BaseRule`
3. Implement required methods:
   ```python
   class NewRule(BaseRule):
       def analyze(self, pdf_path: str) -> AnalysisResult:
           # Implementation
           
       def apply(self, pdf_path: str, output_path: str, 
                 modifications: List[Modification]) -> bool:
           # Implementation
           
       def validate(self, modification: Modification) -> bool:
           # Implementation
   ```
4. Add rule to application (future: rule selection UI)

## Design Patterns

- **Strategy Pattern**: Rules are strategies for APA compliance
- **Factory Pattern**: Model creation (implicit in dataclasses)
- **Observer Pattern**: GUI callbacks for state changes
- **Template Method**: Base rule defines structure, subclasses implement

## Testing Strategy

- **Unit Tests**: Test individual modules in isolation
- **Integration Tests**: Test module interactions
- **GUI Tests**: Test user interactions (future)

## Performance Considerations

- PDF analysis runs in background threads to keep UI responsive
- Format extraction samples first 10 tables for performance
- Large PDFs are processed page by page to manage memory

## Security Considerations

- Input validation for all file paths
- File size limits to prevent DoS
- Safe file operations with proper error handling

