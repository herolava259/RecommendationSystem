

import { Injectable } from "@angular/core";
import { ApiEndpoint,ApiMethod  } from "../../shared/api/api-endpoint.model";
import { IApiEndpointGroup } from "../../shared/api/api.intefaces";


@Injectable()
export class LoginApis implements IApiEndpointGroup {
  name = "Login APIs";
  static readonly LoginPath: ApiEndpoint = {method: ApiMethod.Post, path: '/api/account/login' };
  static readonly LogoutPath: ApiEndpoint = {method: ApiMethod.Post, path: '/api/account/logout' };
}
