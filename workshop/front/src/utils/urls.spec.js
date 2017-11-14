import { API_URL, LINKS_API_URL } from './urls.js';

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

})
