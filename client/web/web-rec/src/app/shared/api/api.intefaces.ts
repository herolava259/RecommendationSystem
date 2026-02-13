import { ApiEndpoint, ApiMethod } from "./api-endpoint.model";


export interface IApiEndpointGroup {
  name: string;
}

export interface IEntity {
  id?: string;
}

export class CrudApiEndpointGroup implements IApiEndpointGroup {

  name!: string;

  createEndpoint?: ApiEndpoint;
  getEndpoint?: ApiEndpoint;
  updateEndpoint?: ApiEndpoint;
  deleteEndpoint?: ApiEndpoint
  partialUpdateEndpoint?: ApiEndpoint;
  listEndpoint?: ApiEndpoint;
  paginationEndpoint?: ApiEndpoint;


  constructor(name: string, ) {
    this.name = name;
    this.createEndpoint = { method: ApiMethod.Post, path: `/api/${name.toLowerCase()}` };
    this.getEndpoint = { method: ApiMethod.Get, path: `/api/${name.toLowerCase()}` };
    this.updateEndpoint = { method: ApiMethod.Put, path: `/api/${name.toLowerCase()}` };
    this.deleteEndpoint = { method: ApiMethod.Delete, path: `/api/${name.toLowerCase()}` };
    this.partialUpdateEndpoint = { method: ApiMethod.Patch, path: `/api/${name.toLowerCase()}` };
    this.listEndpoint = { method: ApiMethod.Get, path: `/api/${name.toLowerCase()}/list` };
    this.paginationEndpoint = { method: ApiMethod.Get, path: `/api/${name.toLowerCase()}/pagination` };
  }

}