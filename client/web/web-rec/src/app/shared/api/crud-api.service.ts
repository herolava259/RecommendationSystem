
import { Observable } from "rxjs";
import { IEntity } from "./api-endpoint.model";
import { CrudApiEndpointGroup } from "./api.intefaces";
import { BaseApiService } from "./base-api.service";

import { HttpClient } from "@angular/common/http";


export abstract class CrudApiService<TEntity extends IEntity> extends BaseApiService<CrudApiEndpointGroup>
{


  constructor(entityName: string, protected override http: HttpClient, apiBaseUrl: string) {
    const endpoints = new CrudApiEndpointGroup(entityName);
    super(endpoints, http, apiBaseUrl);
  }

  public getEntityById(id: string): Observable<TEntity> {
    return this.callApi<null, TEntity>(this.apiEndpointGroup.getEndpoint!, null, { id });
  }

  public createEntity(entity: TEntity): Observable<TEntity> {
    return this.callApi<TEntity, TEntity>(this.apiEndpointGroup.createEndpoint!, entity);
  }

  public updateEntity(entity: TEntity): Observable<{success: boolean; entity: TEntity}> {
    return this.callApi<TEntity, {success: boolean; entity: TEntity}>(this.apiEndpointGroup.updateEndpoint!, entity);
  }

  public deleteEntityById(id: string): Observable<boolean> {
    return this.callApi<null, boolean>(this.apiEndpointGroup.deleteEndpoint!, null, { id });
  }

  public listEntities(): Observable<TEntity[]> {
    return this.callApi<null, TEntity[]>(this.apiEndpointGroup.listEndpoint!);
  }

  public partialUpdateEntity(entity: Partial<TEntity> & { id: string }): Observable<boolean> {
    return this.callApi<Partial<TEntity> & { id: string }, boolean>(this.apiEndpointGroup.partialUpdateEndpoint!, entity);
  }

  // TODO: Implement pagination method later

}