import { HttpClient, HttpHeaders, HttpParams } from "@angular/common/http";
import { IApiEndpointGroup } from "./api.intefaces";
import { Observable, tap } from "rxjs";
import { Inject } from "@angular/core";
import { API_BASE_URL } from "../../app.di.tokens";
import { ApiEndpoint, ApiMethod } from "./api-endpoint.model";

export type IApiParams = Record<string, string | number | boolean>;

export abstract class BaseApiService<TApiEndpointGroup extends IApiEndpointGroup> {

  constructor(protected apiEndpointGroup: TApiEndpointGroup, protected http: HttpClient,
    @Inject(API_BASE_URL) protected apiBaseUrl: string
  ) {}

  private createHttpParams(params?: IApiParams | null) : HttpParams
  {
    let httpParams = new HttpParams();

    if(params === null || params === undefined){
      return httpParams;
    }

    Object.entries(params).forEach( ([key, value]) => {
      if (value !== null && value !== undefined){
        httpParams = httpParams.set(key, value.toString());
      }
    });
    return httpParams;
  }

  private createHttpHeaders(headers?: object | null) : HttpHeaders
  {
    let httpHeaders = new HttpHeaders();

    if(headers === null || headers === undefined){
      return httpHeaders;
    }

    Object.entries(headers).forEach( ([key, value]) => {
      if (value !== null && value !== undefined){
        httpHeaders = httpHeaders.set(key, value.toString());
      }
    });
    return httpHeaders
  }

  protected callApi<TBody,TResponse>(endpoint: ApiEndpoint, body: TBody | null = null, params: IApiParams | null = null, headers: object | null = {}): Observable<TResponse>{
    switch(endpoint.method){
      case ApiMethod.Get: return this.get<TResponse>(endpoint.path, params, headers);
      case ApiMethod.Post: return this.post<TBody, TResponse>(endpoint.path, body, params, headers);
      case ApiMethod.Put: return this.put<TBody, TResponse>(endpoint.path, body, params, headers);
      case ApiMethod.Patch: return this.patch<TBody, TResponse>(endpoint.path, body, params, headers);
      case ApiMethod.Delete: return this.delete<TResponse>(endpoint.path, params, headers);
      default: throw new Error(`Unsupported API method: ${endpoint.method}`);
    }
  }

  protected get<TResponse>(path: string, params?: IApiParams | null, headers?: object | null): Observable<TResponse>{

    return this.http.get<TResponse>(`${this.apiBaseUrl}/${path}`, {params: this.createHttpParams(params), headers: this.createHttpHeaders(headers)})
                      .pipe(tap(response => {
                        // You can add logging or other side effects here if needed
                        console.log(`GET ${path} response:`, response);
                      }));
  }

  protected post<TBody, TResponse>(path: string, body?: TBody | null, params?: IApiParams | null, headers?: object | null): Observable<TResponse>{
    return this.http.post<TResponse>(`${this.apiBaseUrl}/${path}`, body, {params: this.createHttpParams(params), headers: this.createHttpHeaders(headers)})
                      .pipe(tap(response => {
                        // You can add logging or other side effects here if needed
                        console.log(`POST ${path} response:`, response);
                      }));
  }


  protected put<TBody, TResponse>(path:string, body?: TBody | null, params?: IApiParams | null, headers?: object | null): Observable<TResponse>{
    return this.http.put<TResponse>(`${this.apiBaseUrl}/${path}`, body, {params: this.createHttpParams(params), headers: this.createHttpHeaders(headers)});
  }

  protected patch<TBody, TResponse>(path: string, body?: TBody | null, params?: IApiParams | null, headers?: object | null): Observable<TResponse>{
    return this.http.patch<TResponse>(`${this.apiBaseUrl}/${path}`, body, {params: this.createHttpParams(params), headers: this.createHttpHeaders(headers)});
  }

  protected delete<TResponse>(path: string, params?: IApiParams | null, headers?: object | null): Observable<TResponse>{
    return this.http.delete<TResponse>(`${this.apiBaseUrl}/${path}`, {params: this.createHttpParams(params), headers: this.createHttpHeaders(headers)});
  }

}
