import { HttpClient } from "@angular/common/http";
import { IApiEndpointGroup } from "./api.intefaces";
import { BaseApiService, IApiParams } from "./base-api.service";
import { API_BASE_URL, API_RESILIENCY_CONFIG } from "../../app.di.tokens";
import { Inject } from "@angular/core";
import { Observable, retry, timeout, timer } from "rxjs";
import { ApiEndpoint } from "./api-endpoint.model";
import { ResilencyHttpConfig } from "../../configurations/http.config";


export abstract class ApiResilencyService<TApiEndpointGroup extends IApiEndpointGroup> extends BaseApiService<TApiEndpointGroup> {

  constructor(protected override apiEndpointGroup: TApiEndpointGroup, protected override http: HttpClient,
    @Inject(API_BASE_URL) protected override apiBaseUrl: string,
    @Inject(API_RESILIENCY_CONFIG) protected resilencyConfig: ResilencyHttpConfig
  ) {
    super(apiEndpointGroup, http, apiBaseUrl);
  }

  protected override callApi<TBody,TResponse>(endpoint: ApiEndpoint, body: TBody | null = null, params: IApiParams | null = null, headers: object | null = {}): Observable<TResponse>{
    return super.callApi<TBody, TResponse>(endpoint , body, params, headers).pipe(
      timeout(this.resilencyConfig.timeoutSeconds * 1000),
      retry({
        count: this.resilencyConfig.maxRetryAttempts,
        delay: (error, retryCount) => {
          return timer(1000 * retryCount);
        }
      })
    );
  }

  private decorateWithResilency<TResponse>(observable: Observable<TResponse>): Observable<TResponse>
  {
    return observable.pipe(
      timeout(this.resilencyConfig.timeoutSeconds * 1000),
      retry({
        count: this.resilencyConfig.maxRetryAttempts,
        delay: (error, retryCount) => {
          return timer(1000 * retryCount);
        }
      })
    );
  }

  protected override get<TResponse>(path: string, params?: IApiParams | null, headers?: object | null): Observable<TResponse>{

     return this.decorateWithResilency(super.get<TResponse>(path, params, headers));
  }

  protected override post<TBody, TResponse>(path: string, body?: TBody | null, params?: IApiParams | null, headers?: object | null): Observable<TResponse>
  {
    return this.decorateWithResilency(super.post<TBody, TResponse>(path, body, params, headers));
  }


  protected override put<TBody, TResponse>(path:string, body?: TBody | null, params?: IApiParams | null, headers?: object | null): Observable<TResponse>
  {
    return this.decorateWithResilency(super.put<TBody, TResponse>(path, body, params, headers));
  }

  protected override patch<TBody, TResponse>(path: string, body?: TBody | null, params?: IApiParams | null, headers?: object | null): Observable<TResponse>
  {
    return this.decorateWithResilency(super.patch<TBody, TResponse>(path, body, params, headers));
  }

  protected override delete<TResponse>(path: string, params?: IApiParams | null, headers?: object | null): Observable<TResponse>
  {
    return this.decorateWithResilency(super.delete<TResponse>(path, params, headers));
  }
}
