// SimplifiedBlocks JSON Editor with Monaco

let editor = null;
let currentConfig = null;
let showDefaults = true;

// Level 1 Wizard template config (embedded, no API call needed)
const LEVEL_1_WIZARD_CONFIG = {
    "classes": {
        "class_levels": {
            "Wizard": 1
        }
    },
  "block_type": "SimplifiedBlocks"
};

// Initialize Monaco Editor
require.config({ paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' } });

require(['vs/editor/editor.main'], async function() {
    await init();
});

async function init() {
    // Initialize Monaco Editor
    initEditor();

    // Load JSON schema for validation
    await loadSchema();

    // Setup event listeners
    setupEventListeners();

    // Load default template
    loadDefaultConfig();
}

// Initialize Monaco Editor
function initEditor() {
    // Create editor instance
    editor = monaco.editor.create(document.getElementById('editor-container'), {
        value: '{}',
        language: 'json',
        theme: 'vs-dark',
        automaticLayout: true,
        minimap: { enabled: false },
        fontSize: 14,
        formatOnPaste: true,
        formatOnType: true,
        scrollBeyondLastLine: false,
    });

    // Listen for content changes
    editor.onDidChangeModelContent(() => {
        validateJSON();
    });
}

// Load JSON schema from static file (pre-generated during build)
async function loadSchema() {
    try {
        const response = await fetch('/static/simplified-blocks-schema.json');
        if (!response.ok) {
            console.warn('Schema not available:', response.statusText);
            return;
        }

        const schema = await response.json();

        // Configure Monaco JSON validation
        monaco.languages.json.jsonDefaults.setDiagnosticsOptions({
            validate: true,
            schemaValidation: 'error',
            allowComments: false,
            schemas: [{
                uri: "http://dnd-character-creator.local/simplified-blocks.schema.json",
                fileMatch: ["*"],
                schema: schema
            }]
        });

        console.log('✓ Schema validation enabled (pre-generated at build time)');
    } catch (error) {
        console.warn('Schema loading failed:', error);
    }
}

// Setup event listeners
function setupEventListeners() {
    const showDefaultsToggle = document.getElementById('showDefaultsToggle');
    const buildBtn = document.getElementById('buildBtn');
    const saveBtn = document.getElementById('saveBtn');
    const loadBtn = document.getElementById('loadBtn');

    showDefaultsToggle.addEventListener('change', toggleDefaults);
    buildBtn.addEventListener('click', buildCharacter);
    saveBtn.addEventListener('click', saveConfiguration);
    loadBtn.addEventListener('click', loadConfiguration);
}

// Load default config
function loadDefaultConfig() {
    currentConfig = LEVEL_1_WIZARD_CONFIG;
    editor.setValue(JSON.stringify(LEVEL_1_WIZARD_CONFIG, null, 2));
}

// Toggle between showing/hiding defaults
async function toggleDefaults(e) {
    showDefaults = e.target.checked;

    // Try to parse current editor content and reformat it
    try {
        const current = JSON.parse(editor.getValue());

        // Call backend to validate and reformat with or without defaults
        const formatted = await formatWithDefaults(current, showDefaults);
        if (formatted) {
            editor.setValue(JSON.stringify(formatted, null, 2));
        }
    } catch (error) {
        // Invalid JSON, do nothing
        console.error('Failed to toggle defaults:', error);
    }
}

// Format config with or without defaults via backend
async function formatWithDefaults(config, showDefaults) {
    try {
        const response = await fetch(`/format_simplified?show_defaults=${showDefaults}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        });

        if (response.ok) {
            return await response.json();
        } else {
            console.error('Format failed:', await response.text());
            return null;
        }
    } catch (error) {
        console.error('Failed to format:', error);
        return null;
    }
}

// Validate JSON
function validateJSON() {
    const statusDiv = document.getElementById('validation-status');

    try {
        const json = JSON.parse(editor.getValue());

        // Basic validation checks
        if (!json.classes || !json.classes.class_levels) {
            throw new Error('classes.class_levels is required');
        }

        // Success
        statusDiv.className = 'validation-status success';
        statusDiv.textContent = '✓ Valid SimplifiedBlocks configuration';
        return true;
    } catch (error) {
        statusDiv.className = 'validation-status error';
        statusDiv.textContent = `✗ ${error.message}`;
        return false;
    }
}

// Build character
async function buildCharacter() {
    const buildOutput = document.getElementById('buildOutput');
    const buildResults = document.getElementById('buildResults');

    // Validate first
    if (!validateJSON()) {
        alert('Please fix validation errors before building');
        return;
    }

    const config = JSON.parse(editor.getValue());

    buildOutput.innerHTML = '<div class="loading">Building character...</div>';
    buildResults.style.display = 'block';
    buildResults.scrollIntoView({ behavior: 'smooth' });

    try {
        const response = await fetch('/create_character', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                building_blocks: config,
                increment_chain: {}
            })
        });

        const result = await response.json();

        if (response.ok && result.character) {
            buildOutput.innerHTML = `
                <div class="success">
                    <h3>✅ Character Created Successfully!</h3>
                    <div class="character-summary">
                        <p><strong>Name:</strong> ${result.character.name || 'N/A'}</p>
                        <p><strong>Race:</strong> ${result.character.race || 'N/A'}</p>
                        <p><strong>Level:</strong> ${result.character.level || 'N/A'}</p>
                        <p><strong>Classes:</strong> ${formatClasses(result.character.classes)}</p>
                    </div>
                    <details>
                        <summary>View Full Character JSON</summary>
                        <pre>${JSON.stringify(result.character, null, 2)}</pre>
                    </details>
                    <details>
                        <summary>View Increment Chain</summary>
                        <pre>${JSON.stringify(result.increment_chain, null, 2)}</pre>
                    </details>
                </div>
            `;
        } else {
            buildOutput.innerHTML = `
                <div class="error">
                    <h3>❌ Build Failed</h3>
                    <pre>${result.detail || result.error || JSON.stringify(result, null, 2)}</pre>
                </div>
            `;
        }
    } catch (error) {
        buildOutput.innerHTML = `
            <div class="error">
                <h3>❌ Error</h3>
                <p>${error.message}</p>
            </div>
        `;
    }
}

// Format classes for display
function formatClasses(classes) {
    if (!classes) return 'N/A';
    return Object.entries(classes)
        .map(([cls, level]) => `${cls} ${level}`)
        .join(', ');
}

// Save configuration to localStorage
function saveConfiguration() {
    if (!validateJSON()) {
        alert('Cannot save invalid configuration');
        return;
    }

    const config = editor.getValue();
    const name = prompt('Configuration name:');
    if (name) {
        localStorage.setItem(`simplified_config_${name}`, config);
        alert('✅ Configuration saved!');
    }
}

// Load configuration from localStorage
function loadConfiguration() {
    const configs = Object.keys(localStorage)
        .filter(k => k.startsWith('simplified_config_'))
        .map(k => k.replace('simplified_config_', ''));

    if (configs.length === 0) {
        alert('No saved configurations found');
        return;
    }

    const name = prompt(`Available configs:\n${configs.join('\n')}\n\nEnter name to load:`);
    if (name) {
        const config = localStorage.getItem(`simplified_config_${name}`);
        if (config) {
            editor.setValue(config);
        }
    }
}
