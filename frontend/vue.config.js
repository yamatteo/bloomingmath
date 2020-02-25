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
    // proxy: 'http://localhost:8000',
    proxy: {
      "/contents": {
        target: "http://localhost:8000",
        changeOrigin: true,
        timeout: 5000
      },
      "/users": {
        target: "http://localhost:8000",
        changeOrigin: true
      },
      "/groups": {
        target: "http://localhost:8000",
        changeOrigin: true
      },
      "/nodes": {
        target: "http://localhost:8000",
        changeOrigin: true
      }
    }
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
