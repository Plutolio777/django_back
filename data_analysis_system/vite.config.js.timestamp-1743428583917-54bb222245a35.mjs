// vite.config.js
import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "file:///D:/lyj/SourceCodeRepository/data_analysis_system/node_modules/vite/dist/node/index.js";
import vue from "file:///D:/lyj/SourceCodeRepository/data_analysis_system/node_modules/@vitejs/plugin-vue/dist/index.mjs";
import VueDevTools from "file:///D:/lyj/SourceCodeRepository/data_analysis_system/node_modules/vite-plugin-vue-devtools/dist/vite.mjs";
import legacy from "file:///D:/lyj/SourceCodeRepository/data_analysis_system/node_modules/@vitejs/plugin-legacy/dist/index.mjs";
var __vite_injected_original_import_meta_url = "file:///D:/lyj/SourceCodeRepository/data_analysis_system/vite.config.js";
var vite_config_default = defineConfig({
  base: "./",
  plugins: [
    vue(),
    VueDevTools(),
    legacy({
      targets: ["defaults", "not IE 11"]
    })
    // ViteAliases()
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", __vite_injected_original_import_meta_url)),
      "@images": fileURLToPath(new URL("./src/assets/images", __vite_injected_original_import_meta_url)),
      "@style": fileURLToPath(new URL("./src/style", __vite_injected_original_import_meta_url)),
      "@views": fileURLToPath(new URL("./src/views", __vite_injected_original_import_meta_url)),
      "@assets": fileURLToPath(new URL("./src/assets", __vite_injected_original_import_meta_url))
    }
  },
  build: {
    rollupOptions: {
      output: {
        entryFileNames: "static/js/[name]-[hash].js",
        chunkFileNames: "static/js/[name]-[hash].js",
        assetFileNames(assetInfo) {
          if (assetInfo.name.endsWith(".css")) {
            return "static/css/[name]-[hash].css";
          }
          if (assetInfo.name.endsWith(".css")) {
            return "static/css/[name]-[hash].css";
          }
          const imgExtendList = ["png", ".jpg", ".jpeg", ".svg", ".webp", ".gif", ".ico"];
          if (imgExtendList.some((ext) => {
            assetInfo.name.endsWith(ext);
          })) {
            return "static/images/[name]-[hash].[ext]";
          }
          return "static/assets/[name]-[hash].[ext]";
        }
      }
    }
  },
  server: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true
      },
      "/static": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true
      },
      "/media": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true
      }
    }
  }
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcuanMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCJEOlxcXFxseWpcXFxcU291cmNlQ29kZVJlcG9zaXRvcnlcXFxcZGF0YV9hbmFseXNpc19zeXN0ZW1cIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZmlsZW5hbWUgPSBcIkQ6XFxcXGx5alxcXFxTb3VyY2VDb2RlUmVwb3NpdG9yeVxcXFxkYXRhX2FuYWx5c2lzX3N5c3RlbVxcXFx2aXRlLmNvbmZpZy5qc1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9pbXBvcnRfbWV0YV91cmwgPSBcImZpbGU6Ly8vRDovbHlqL1NvdXJjZUNvZGVSZXBvc2l0b3J5L2RhdGFfYW5hbHlzaXNfc3lzdGVtL3ZpdGUuY29uZmlnLmpzXCI7aW1wb3J0IHsgZmlsZVVSTFRvUGF0aCwgVVJMIH0gZnJvbSAnbm9kZTp1cmwnXG5cbmltcG9ydCB7IGRlZmluZUNvbmZpZyB9IGZyb20gJ3ZpdGUnXG5pbXBvcnQgdnVlIGZyb20gJ0B2aXRlanMvcGx1Z2luLXZ1ZSdcbmltcG9ydCBWdWVEZXZUb29scyBmcm9tICd2aXRlLXBsdWdpbi12dWUtZGV2dG9vbHMnXG5pbXBvcnQgbGVnYWN5IGZyb20gJ0B2aXRlanMvcGx1Z2luLWxlZ2FjeSc7XG5cbi8vIGh0dHBzOi8vdml0ZWpzLmRldi9jb25maWcvXG5leHBvcnQgZGVmYXVsdCBkZWZpbmVDb25maWcoe1xuICBiYXNlOlwiLi9cIixcbiAgcGx1Z2luczogW1xuICAgIHZ1ZSgpLFxuICAgIFZ1ZURldlRvb2xzKCksXG4gICAgbGVnYWN5KHtcbiAgICAgIHRhcmdldHM6W1wiZGVmYXVsdHNcIixcIm5vdCBJRSAxMVwiXSxcbiAgICB9KVxuICAgIC8vIFZpdGVBbGlhc2VzKClcbiAgXSxcbiAgcmVzb2x2ZToge1xuICAgIGFsaWFzOiB7XG4gICAgICAnQCc6IGZpbGVVUkxUb1BhdGgobmV3IFVSTCgnLi9zcmMnLCBpbXBvcnQubWV0YS51cmwpKSxcbiAgICAgICdAaW1hZ2VzJzogZmlsZVVSTFRvUGF0aChuZXcgVVJMKCcuL3NyYy9hc3NldHMvaW1hZ2VzJyxpbXBvcnQubWV0YS51cmwpKSxcbiAgICAgICdAc3R5bGUnOiBmaWxlVVJMVG9QYXRoKG5ldyBVUkwoJy4vc3JjL3N0eWxlJyxpbXBvcnQubWV0YS51cmwpKSxcbiAgICAgICdAdmlld3MnOiBmaWxlVVJMVG9QYXRoKG5ldyBVUkwoJy4vc3JjL3ZpZXdzJyxpbXBvcnQubWV0YS51cmwpKSxcbiAgICAgICdAYXNzZXRzJzogZmlsZVVSTFRvUGF0aChuZXcgVVJMKCcuL3NyYy9hc3NldHMnLGltcG9ydC5tZXRhLnVybCkpLFxuICAgIH1cbiAgfSxcbiAgYnVpbGQ6IHtcbiAgICByb2xsdXBPcHRpb25zOntcbiAgICAgIG91dHB1dDoge1xuICAgICAgICBlbnRyeUZpbGVOYW1lczpcInN0YXRpYy9qcy9bbmFtZV0tW2hhc2hdLmpzXCIsXG4gICAgICAgIGNodW5rRmlsZU5hbWVzOlwic3RhdGljL2pzL1tuYW1lXS1baGFzaF0uanNcIixcbiAgICAgICAgYXNzZXRGaWxlTmFtZXMoYXNzZXRJbmZvKSB7XG4gICAgICAgICAgaWYgKGFzc2V0SW5mby5uYW1lLmVuZHNXaXRoKFwiLmNzc1wiKSkge1xuICAgICAgICAgICAgcmV0dXJuIFwic3RhdGljL2Nzcy9bbmFtZV0tW2hhc2hdLmNzc1wiO1xuICAgICAgICAgIH1cbiAgICAgICAgICBpZiAoYXNzZXRJbmZvLm5hbWUuZW5kc1dpdGgoXCIuY3NzXCIpKSB7XG4gICAgICAgICAgICByZXR1cm4gXCJzdGF0aWMvY3NzL1tuYW1lXS1baGFzaF0uY3NzXCI7XG4gICAgICAgICAgfVxuICAgICAgICAgIGNvbnN0IGltZ0V4dGVuZExpc3QgPSBbXCJwbmdcIiwgXCIuanBnXCIsIFwiLmpwZWdcIiwgXCIuc3ZnXCIsIFwiLndlYnBcIiwgXCIuZ2lmXCIsIFwiLmljb1wiXVxuICAgICAgICAgIGlmIChpbWdFeHRlbmRMaXN0LnNvbWUoZXh0ID0+IHtcbiAgICAgICAgICAgIGFzc2V0SW5mby5uYW1lLmVuZHNXaXRoKGV4dClcbiAgICAgICAgICB9KSkge1xuICAgICAgICAgICAgcmV0dXJuIFwic3RhdGljL2ltYWdlcy9bbmFtZV0tW2hhc2hdLltleHRdXCI7XG4gICAgICAgICAgfVxuICAgICAgICAgIHJldHVybiBcInN0YXRpYy9hc3NldHMvW25hbWVdLVtoYXNoXS5bZXh0XVwiO1xuXG4gICAgICAgIH0sXG4gICAgICB9XG4gICAgfVxuICB9LFxuICBzZXJ2ZXI6IHtcbiAgICBwcm94eToge1xuICAgICAgJy9hcGknOiB7XG4gICAgICAgIHRhcmdldDogJ2h0dHA6Ly8xMjcuMC4wLjE6ODAwMCcsXG4gICAgICAgIGNoYW5nZU9yaWdpbjogdHJ1ZSxcblxuICAgICAgfSxcbiAgICAgIFwiL3N0YXRpY1wiOntcbiAgICAgICAgdGFyZ2V0OiAnaHR0cDovLzEyNy4wLjAuMTo4MDAwJyxcbiAgICAgICAgY2hhbmdlT3JpZ2luOiB0cnVlLFxuICAgICAgfSxcbiAgICAgIFwiL21lZGlhXCI6e1xuICAgICAgICB0YXJnZXQ6ICdodHRwOi8vMTI3LjAuMC4xOjgwMDAnLFxuICAgICAgICBjaGFuZ2VPcmlnaW46IHRydWUsXG4gICAgICB9XG5cbiAgICB9XG4gIH1cbn0pXG4iXSwKICAibWFwcGluZ3MiOiAiO0FBQTBVLFNBQVMsZUFBZSxXQUFXO0FBRTdXLFNBQVMsb0JBQW9CO0FBQzdCLE9BQU8sU0FBUztBQUNoQixPQUFPLGlCQUFpQjtBQUN4QixPQUFPLFlBQVk7QUFMNEwsSUFBTSwyQ0FBMkM7QUFRaFEsSUFBTyxzQkFBUSxhQUFhO0FBQUEsRUFDMUIsTUFBSztBQUFBLEVBQ0wsU0FBUztBQUFBLElBQ1AsSUFBSTtBQUFBLElBQ0osWUFBWTtBQUFBLElBQ1osT0FBTztBQUFBLE1BQ0wsU0FBUSxDQUFDLFlBQVcsV0FBVztBQUFBLElBQ2pDLENBQUM7QUFBQTtBQUFBLEVBRUg7QUFBQSxFQUNBLFNBQVM7QUFBQSxJQUNQLE9BQU87QUFBQSxNQUNMLEtBQUssY0FBYyxJQUFJLElBQUksU0FBUyx3Q0FBZSxDQUFDO0FBQUEsTUFDcEQsV0FBVyxjQUFjLElBQUksSUFBSSx1QkFBc0Isd0NBQWUsQ0FBQztBQUFBLE1BQ3ZFLFVBQVUsY0FBYyxJQUFJLElBQUksZUFBYyx3Q0FBZSxDQUFDO0FBQUEsTUFDOUQsVUFBVSxjQUFjLElBQUksSUFBSSxlQUFjLHdDQUFlLENBQUM7QUFBQSxNQUM5RCxXQUFXLGNBQWMsSUFBSSxJQUFJLGdCQUFlLHdDQUFlLENBQUM7QUFBQSxJQUNsRTtBQUFBLEVBQ0Y7QUFBQSxFQUNBLE9BQU87QUFBQSxJQUNMLGVBQWM7QUFBQSxNQUNaLFFBQVE7QUFBQSxRQUNOLGdCQUFlO0FBQUEsUUFDZixnQkFBZTtBQUFBLFFBQ2YsZUFBZSxXQUFXO0FBQ3hCLGNBQUksVUFBVSxLQUFLLFNBQVMsTUFBTSxHQUFHO0FBQ25DLG1CQUFPO0FBQUEsVUFDVDtBQUNBLGNBQUksVUFBVSxLQUFLLFNBQVMsTUFBTSxHQUFHO0FBQ25DLG1CQUFPO0FBQUEsVUFDVDtBQUNBLGdCQUFNLGdCQUFnQixDQUFDLE9BQU8sUUFBUSxTQUFTLFFBQVEsU0FBUyxRQUFRLE1BQU07QUFDOUUsY0FBSSxjQUFjLEtBQUssU0FBTztBQUM1QixzQkFBVSxLQUFLLFNBQVMsR0FBRztBQUFBLFVBQzdCLENBQUMsR0FBRztBQUNGLG1CQUFPO0FBQUEsVUFDVDtBQUNBLGlCQUFPO0FBQUEsUUFFVDtBQUFBLE1BQ0Y7QUFBQSxJQUNGO0FBQUEsRUFDRjtBQUFBLEVBQ0EsUUFBUTtBQUFBLElBQ04sT0FBTztBQUFBLE1BQ0wsUUFBUTtBQUFBLFFBQ04sUUFBUTtBQUFBLFFBQ1IsY0FBYztBQUFBLE1BRWhCO0FBQUEsTUFDQSxXQUFVO0FBQUEsUUFDUixRQUFRO0FBQUEsUUFDUixjQUFjO0FBQUEsTUFDaEI7QUFBQSxNQUNBLFVBQVM7QUFBQSxRQUNQLFFBQVE7QUFBQSxRQUNSLGNBQWM7QUFBQSxNQUNoQjtBQUFBLElBRUY7QUFBQSxFQUNGO0FBQ0YsQ0FBQzsiLAogICJuYW1lcyI6IFtdCn0K
