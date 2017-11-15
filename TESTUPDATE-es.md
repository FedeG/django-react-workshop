# Actualizar testing para las nuevas funcionalidades

## Tests de nuevas urls
En **workshop/front/src/utils/urls.spec.js**:
```javascript
-import { API_URL, LINKS_API_URL } from './urls.js';
+import { API_URL, LINKS_API_URL, WS_URL, LINKS_WS_URL } from './urls.js';

 ...

 describe('Url utils', () => {

   ...

+  describe('WS_URL', () => {
+
+    it('should is WS_URL is ws://localhost:5000/', () => {
+      expect(WS_URL).toEqual('ws://localhost:5000/');
+    })
+
+  })
+
+  describe('LINKS_WS_URL', () => {
+
+    it('should is LINKS_WS_URL is ws://localhost:5000/update/links/', () => {
+      expect(LINKS_WS_URL).toEqual('ws://localhost:5000/update/links/');
+    })
+
+  })
+
 })
```
