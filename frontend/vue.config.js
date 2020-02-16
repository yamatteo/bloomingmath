module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],

  // CUSTOM
  pwa: {
    name: 'App name',
    themeColor: '#550099',
    msTileColor: '#FFFFFF',
    manifestOptions: {
      background_color: '#550099'
    }
  },

  outputDir: '../dist',
  assetsDir: 'static'
}