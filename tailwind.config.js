module.exports = {
    content: [
        "../backend/templates/**/*.html",  // Para detectar clases dentro de Django templates
        "./src/**/*.html",                 // Para detectar clases en frontend
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/aspect-ratio'),
        require('@tailwindcss/typography'),
    ],
}
