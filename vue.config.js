const { defineConfig } = require('@vue/cli-service')
const path = require('path');

module.exports = defineConfig({
  transpileDependencies: true,
  chainWebpack: config => {
    config.resolve.alias
      .set('@', path.resolve(__dirname, 'app'));  // 'app' is the new folder
  },
  configureWebpack: {
    entry: './app/main.js'  // Set entry point to 'app/main.js'
  }
})
