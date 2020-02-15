module.exports = {
  publicPath: "/static/",
  assetsDir: "assets",
  devServer: {
    contentBase: "src",
    compress: true,
    port: 8080,
    watchOptions: {
      poll: true,
    },
    proxy: 'http://localhost:8000',
  },
  outputDir: "../dist",
  // CUSTOM looks like this is the way to specify the page title?
  // pages: {
  //   index: {
  //     chunks: ['chunk-vendors', 'chunk-common', 'index'],
  //     entry: 'src/main.js',
  //     filename: 'index.html',
  //     template: 'public/index.html',
  //     title: 'Bloomingmath',
  //   },
  // },
  // CUSTOM this to make the app mobile friendly
  // pwa: {
  //   name: 'Bloomingmath',
  //   themeColor: '#F8F8F8',
  //   msTileColor: '#F8F8F8',
  //   appleMobileWebAppCapable: 'yes',
  //   appleMobileWebAppStatusBarStyle: 'black',

  //   // configure the workbox plugin
  //   workboxPluginMode: 'InjectManifest',
  //   workboxOptions: {
  //     // swSrc is required in InjectManifest mode.
  //     swSrc: 'dev/sw.js',
  //     // ...other Workbox options...
  //   }
  // }
};