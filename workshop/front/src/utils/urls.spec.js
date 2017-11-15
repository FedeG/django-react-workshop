import { API_URL, LINKS_API_URL, WS_URL, LINKS_WS_URL } from './urls.js';

describe('Url utils', () => {

  describe('API_URL', () => {

    it('should API_URL is /links/api/', () => {
      expect(API_URL).toEqual('/links/api/');
    })

  })

  describe('LINKS_API_URL', () => {

    it('should LINKS_API_URL is /links/api/links/', () => {
      expect(LINKS_API_URL).toEqual('/links/api/links/');
    })

  })

  describe('WS_URL', () => {

    it('should is WS_URL is ws://localhost:5000/', () => {
      expect(WS_URL).toEqual('ws://localhost:5000/');
    })

  })

  describe('LINKS_WS_URL', () => {

    it('should is LINKS_WS_URL is ws://localhost:5000/update/links/', () => {
      expect(LINKS_WS_URL).toEqual('ws://localhost:5000/updates/links/');
    })

  })

})
