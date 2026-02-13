
export type ApiEndpointMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

export interface ApiEndpoint {

  method: ApiEndpointMethod;
  path: string;
}


export class ApiMethod {
  static readonly Get: ApiEndpointMethod = 'GET';
  static readonly Post: ApiEndpointMethod = 'POST'
  static readonly Put: ApiEndpointMethod = 'PUT';
  static readonly Delete: ApiEndpointMethod = 'DELETE';
  static readonly Patch: ApiEndpointMethod = 'PATCH';
}


export interface IEntity {
  id: string;
}
