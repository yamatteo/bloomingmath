module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  devServer: {
    contentBase: "src",
    compress: true,
    port: 8080,
    watchOptions: {
      poll: true,
    },
    proxy: 'http://localhost:8000',
  },

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
  publicPath: "/static/"
}
