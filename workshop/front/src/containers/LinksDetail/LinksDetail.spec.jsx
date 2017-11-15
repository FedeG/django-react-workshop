import React from 'react';
import LinksDetail from './index.jsx';
import { shallow } from 'enzyme';

describe('LinksDetail Component', () => {
  let links, link, LinksDetailContainerWrapper, LinksDetailContainer;

  beforeAll(() => {
    link = {
      model: 'links.link',
      pk: 1,
      fields: {
        name: 'Gitlab with workshop',
        url: 'https://gitlab.com/FedeG/django-react-workshop/',
        pending: false,
        description: '',
        user: 1
      }
    }
    links = [link]
  })

  describe('props', () => {

    it('should declare propsTypes', () => {
      expect(Object.keys(LinksDetail.propTypes)).toHaveLength(1);
      expect(LinksDetail.propTypes).toHaveProperty('links');
    })

  })

  describe('#render', () => {

    it('should render the component properly', () => {
      const wrapper = shallow(<LinksDetail links={links}/>);
      const itemInDOM = `<p>${link.fields.name}: <a href="${link.fields.url}">${link.fields.url}</a></p>`;
      const button = '<button class="btn btn-success" type="button">Refresh</button>';
      const componentInDOM = `<div><div class="container"><div class="row"><div class="col-sm-12"><h1>Links</h1>${button}<div style="margin-top:20px">${itemInDOM}</div></div></div></div><div></div></div>`;
      expect(wrapper.html()).toBe(componentInDOM);
    })

  })

  describe('state', () => {
    let linkEvent, linkUpdate, linkCreate, linkDelete;

    beforeAll(() => {
      linkEvent = {
        stream: 'links',
        payload: {
          action: 'update',
          pk: 1,
          data: {
            name: 'Extra fields on many to many',
            url: 'https://docs.djangoproject.com/en/1.11/topics/db/models/#extra-fields-on-many-to-many-relationships',
            pending: false,
            description: '',
            user: 1
          },
          model: 'links.link'
        }
      };
      linkUpdate = JSON.parse(JSON.stringify(linkEvent));
      linkCreate = JSON.parse(JSON.stringify(linkEvent));
      linkCreate.payload.action = 'create';
      linkDelete = JSON.parse(JSON.stringify(linkEvent));
      linkDelete.payload.action = 'delete';
    })

    beforeEach(() => {
      LinksDetailContainerWrapper = shallow(<LinksDetail links={links}/>);
      LinksDetailContainer = LinksDetailContainerWrapper.instance();
    })

    it('should state have links', () => {
      expect(LinksDetailContainer.state).toHaveProperty('links');
      expect(LinksDetailContainer.state.links).toEqual(links);
    })

    it('when send link create event onUpdate should update link', () => {
      const updatedLink = LinksDetailContainer.getLink(
        linkUpdate.payload.pk, linkUpdate.payload.data
      )
      const expectedLinks = [updatedLink];
      LinksDetailContainer._onUpdate(JSON.stringify(linkUpdate));
      expect(LinksDetailContainer.state).toHaveProperty('links');
      expect(LinksDetailContainer.state.links).toEqual(expectedLinks);
    })

    it('when send link create event onUpdate should append link', () => {
      const createdLink = LinksDetailContainer.getLink(
        linkUpdate.payload.pk, linkUpdate.payload.data
      )
      const expectedLinks = [...links, createdLink];
      LinksDetailContainer._onUpdate(JSON.stringify(linkCreate));
      expect(LinksDetailContainer.state).toHaveProperty('links');
      expect(LinksDetailContainer.state.links).toEqual(expectedLinks);
    })

    it('when send link delete event onUpdate should remove link', () => {
      const expectedLinks = [];
      LinksDetailContainer._onUpdate(JSON.stringify(linkDelete));
      expect(LinksDetailContainer.state).toHaveProperty('links');
      expect(LinksDetailContainer.state.links).toEqual(expectedLinks);
    })

  })


})
