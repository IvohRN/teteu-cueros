// JavaScript principal para Teteu Cueros

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidades
    initializeColorSelector();
    initializeHerrajesSelector();
    initializeForm();
});

// Selector de color
function initializeColorSelector() {
    const colorSelect = document.getElementById('colorSelect');
    const colorPreview = document.getElementById('colorPreview');
    
    if (colorSelect && colorPreview) {
        colorSelect.addEventListener('change', function() {
            updateColorPreview(this.value);
            updateCarteraImage();
        });
    }
}

// Selector de herrajes
function initializeHerrajesSelector() {
    const herrajesSelect = document.getElementById('herrajesSelect');
    const herrajesPreview = document.getElementById('herrajesPreview');
    
    if (herrajesSelect && herrajesPreview) {
        herrajesSelect.addEventListener('change', function() {
            updateHerrajesPreview(this.value);
            updateCarteraImage();
        });
    }
}

// Actualizar preview de color
function updateColorPreview(color) {
    const colorPreview = document.getElementById('colorPreview');
    if (!colorPreview) return;
    
    const colorMap = {
        'negro': '/static/colors1.png',
        'marron': '/static/colors2.png',
        'marron claro': '/static/colors3.png'
    };
    
    const imagePath = colorMap[color] || '/static/colors1.png';
    colorPreview.src = imagePath;
}

// Actualizar preview de herrajes
function updateHerrajesPreview(herrajes) {
    const herrajesPreview = document.getElementById('herrajesPreview');
    if (!herrajesPreview) return;
    
    const herrajesMap = {
        'plata': '/static/h1.png',
        'dorado': '/static/h2.png'
    };
    
    const imagePath = herrajesMap[herrajes] || '/static/h1.png';
    herrajesPreview.src = imagePath;
}

// Actualizar imagen de la cartera
function updateCarteraImage() {
    const colorSelect = document.getElementById('colorSelect');
    const herrajesSelect = document.getElementById('herrajesSelect');
    const carteraImg = document.getElementById('carteraImg');
    
    if (!colorSelect || !herrajesSelect || !carteraImg) return;
    
    const color = colorSelect.value;
    const herrajes = herrajesSelect.value;
    
    // Mapear valores a nombres de archivo
    const colorFile = mapColorToFile(color);
    const herrajesFile = mapHerrajesToFile(herrajes);
    
    // Determinar modelo
    const modelo = getCurrentModel();
    
    // Construir ruta de imagen
    const imagePath = `/static/${modelo}_${colorFile}_${herrajesFile}.jpg`;
    
    // Actualizar imagen con efecto de transición
    carteraImg.style.opacity = '0.5';
    carteraImg.src = imagePath;
    
    carteraImg.onload = function() {
        carteraImg.style.opacity = '1';
    };
    
    carteraImg.onerror = function() {
        // Si la imagen no existe, mostrar imagen por defecto
        carteraImg.src = `/static/${modelo}.jpg`;
        carteraImg.style.opacity = '1';
    };
}

// Mapear color a nombre de archivo
function mapColorToFile(color) {
    const colorMap = {
        'negro': 'negro',
        'marron': 'marron',
        'marron claro': 'marron_claro'
    };
    return colorMap[color] || 'negro';
}

// Mapear herrajes a nombre de archivo
function mapHerrajesToFile(herrajes) {
    const herrajesMap = {
        'plata': 'plata',
        'dorado': 'dorado'
    };
    return herrajesMap[herrajes] || 'plata';
}

// Obtener modelo actual
function getCurrentModel() {
    // Obtener modelo de la URL o del contexto
    const urlParams = new URLSearchParams(window.location.search);
    const modelo = urlParams.get('modelo') || '';
    
    if (modelo.toLowerCase().includes('urbana')) {
        return 'modelo2';
    }
    return 'modelo1';
}

// Inicializar formulario
function initializeForm() {
    const form = document.getElementById('personalizarForm');
    if (!form) return;
    
    form.addEventListener('submit', handleFormSubmit);
}

// Manejar envío del formulario
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitButton = form.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    
    try {
        // Mostrar loading
        showLoading(submitButton);
        
        // Validar datos
        const formData = new FormData(form);
        const validationResult = validateFormData(formData);
        
        if (!validationResult.isValid) {
            showError(validationResult.message);
            hideLoading(submitButton, originalText);
            return;
        }
        
        // Enviar datos
        const modelo = getCurrentModel();
        const response = await fetch(`/personalizar?modelo=${encodeURIComponent(modelo)}`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`Error del servidor: ${response.status}`);
        }
        
        const enlace = await response.text();
        
        // Copiar al portapapeles
        await navigator.clipboard.writeText(enlace);
        
        // Mostrar éxito
        showSuccess('¡Enlace copiado al portapapeles!');
        
    } catch (error) {
        console.error('Error:', error);
        showError('Error al procesar la personalización. Inténtalo de nuevo.');
    } finally {
        hideLoading(submitButton, originalText);
    }
}

// Validar datos del formulario
function validateFormData(formData) {
    const color = formData.get('color');
    const herrajes = formData.get('herrajes');
    
    const validColors = ['negro', 'marron', 'marron claro'];
    const validHerrajes = ['plata', 'dorado'];
    
    if (!color || !validColors.includes(color)) {
        return {
            isValid: false,
            message: 'Por favor selecciona un color válido.'
        };
    }
    
    if (!herrajes || !validHerrajes.includes(herrajes)) {
        return {
            isValid: false,
            message: 'Por favor selecciona herrajes válidos.'
        };
    }
    
    return { isValid: true };
}

// Mostrar loading
function showLoading(button) {
    button.disabled = true;
    button.innerHTML = '<span class="loading"></span> Procesando...';
}

// Ocultar loading
function hideLoading(button, originalText) {
    button.disabled = false;
    button.textContent = originalText;
}

// Mostrar mensaje de error
function showError(message) {
    showMessage(message, 'error');
}

// Mostrar mensaje de éxito
function showSuccess(message) {
    showMessage(message, 'success');
}

// Mostrar mensaje
function showMessage(message, type) {
    // Remover mensajes existentes
    const existingMessages = document.querySelectorAll('.error-message, .success-message');
    existingMessages.forEach(msg => msg.remove());
    
    // Crear nuevo mensaje
    const messageDiv = document.createElement('div');
    messageDiv.className = type === 'error' ? 'error-message' : 'success-message';
    messageDiv.textContent = message;
    
    // Insertar mensaje
    const formContainer = document.querySelector('.form-container');
    if (formContainer) {
        formContainer.insertBefore(messageDiv, formContainer.firstChild);
        
        // Auto-remover después de 5 segundos
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.remove();
            }
        }, 5000);
    }
}

// Utilidades adicionales
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Optimización de imágenes
function optimizeImageLoading() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.style.opacity = '1';
        });
    });
}

// Inicializar optimizaciones
document.addEventListener('DOMContentLoaded', function() {
    optimizeImageLoading();
});
