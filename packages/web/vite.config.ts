import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import viteCompression from 'vite-plugin-compression';
import { visualizer } from 'rollup-plugin-visualizer';
import type { PluginOption } from 'vite';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // Load env file based on `mode` in the current working directory.
  const env = loadEnv(mode, process.cwd(), '');
  
  return {
    plugins: [
      react(),
      // Gzip compression
      viteCompression({
        algorithm: 'gzip',
        ext: '.gz',
        threshold: 1024, // Only compress files larger than 1KB
        deleteOriginFile: false,
      }),
      // Brotli compression
      viteCompression({
        algorithm: 'brotliCompress',
        ext: '.br',
        threshold: 1024,
        deleteOriginFile: false,
      }),
      // Bundle analysis - generates stats.html in dist folder
      visualizer({
        open: false,
        gzipSize: true,
        brotliSize: true,
        filename: 'dist/stats.html',
      }) as PluginOption,
    ],

    // Environment variables configuration
    envPrefix: 'VITE_',
    define: {
      // Make some env vars available at build time
      'import.meta.env.VITE_APP_VERSION': JSON.stringify(process.env.npm_package_version),
    },

    build: {
      // Output directory
      outDir: 'dist',
      
      // Generate source maps for debugging
      sourcemap: mode === 'development' ? true : 'hidden',
      
      // Target modern browsers for smaller bundles
      target: 'esnext',
      
      // Minification
      minify: 'esbuild',
      
      // Asset optimization
      assetsInlineLimit: 4096, // 4kb - inline assets smaller than this
      
      // Chunk size warnings
      chunkSizeWarningLimit: 500, // 500kb warning threshold
      
      rollupOptions: {
        output: {
          // Manual chunk splitting for better caching
          manualChunks: {
            // Separate vendor chunks
            'react-vendor': ['react', 'react-dom'],
            // Add more chunks as needed, e.g.:
            // 'ui-vendor': ['@mui/material', '@emotion/react'],
          },
          
          // Asset file naming
          assetFileNames: (assetInfo) => {
            const info = assetInfo.name?.split('.') || [];
            let extType = info[info.length - 1];
            
            // Organize assets by type
            if (/\.(png|jpe?g|svg|gif|tiff|bmp|ico)$/i.test(assetInfo.name || '')) {
              extType = 'img';
            } else if (/\.(woff2?|ttf|eot)$/i.test(assetInfo.name || '')) {
              extType = 'fonts';
            }
            
            return `assets/${extType}/[name]-[hash][extname]`;
          },
          
          // Chunk file naming
          chunkFileNames: 'assets/js/[name]-[hash].js',
          entryFileNames: 'assets/js/[name]-[hash].js',
        },
      },
      
      // CSS code splitting
      cssCodeSplit: true,
    },

    // Development server configuration
    server: {
      port: 3000,
      open: false,
      cors: true,
      // Proxy API requests in development
      proxy: {
        '/api': {
          target: env.VITE_API_URL || 'http://localhost:8000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },
    },

    // Preview server (for testing production build)
    preview: {
      port: 4173,
      open: false,
    },

    // Dependency optimization
    optimizeDeps: {
      include: ['react', 'react-dom'],
    },
  };
});
