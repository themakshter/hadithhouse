/**
 * The MIT License (MIT)
 *
 * Copyright (c) 2016 Rafid Khalid Al-Humaimidi
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

/// <reference path="../../../../../TypeScriptDefs/angularjs/angular.d.ts" />
/// <reference path="../../../../../TypeScriptDefs/angular-material/angular-material.d.ts" />
/// <reference path="../app.ts" />
/// <reference path="../services/services.ts" />
/// <reference path="entity-page.ts" />

module HadithHouse.Controllers {
  import User = HadithHouse.Resources.User;

  export class UserPageCtrl extends EntityPageCtrl<User> {
    private UserResource:Resources.CacheableResource<User, number>;
    private permissions:{};
    private permissionGroups:String[];
    private permissionsNameMap:{};

    constructor($scope:ng.IScope,
                $rootScope:ng.IScope,
                $location:ng.ILocationService,
                $routeParams:any,
                UserResource:Resources.CacheableResource<User, number>) {
      super($scope, $rootScope, $location, $routeParams, UserResource);
      this.UserResource = UserResource;
    }

    protected getEntityPath(id: number) {
      return 'user/' + id;
    }

    protected onEntityLoaded() {
      this.entity.permissionsOrdered = _.sortBy<string>(this.entity.permissions, (a) => {
        let parts = a.split('_');
        return `${parts[1]}_${parts[0]}`;
      });

      let permissions = {};
      let permissionGroups:String[] = [];
      _.each(this.entity.permissions, (a) => {
        let parts = a.split('_');
        let group = parts[1];
        let type = parts[0];
        if (!permissions[group]) {
          permissions[group] = [];
          permissionGroups.push(group);
        }
        permissions[group].push(type);
      });
      _.each(permissions, (value, key) => {
        permissions[key] = _.sortBy<String>(permissions[key]);
      });
      this.permissions = permissions;
      this.permissionGroups = _.sortBy<String>(permissionGroups, p => p);
      this.permissionsNameMap = {
        'book': 'Book',
        'bookchapter': 'Book Chapter',
        'bookvolume': 'Book Volume',
        'booksection': 'Book Section',
        'chain': 'Chain',
        'chainpersonrel': 'Chain-Person Relation',
        'hadith': 'Hadith',
        'hadithtag': 'Hadith Tag',
        'hadithtagrel': 'Hadith-Tag Relation',
        'person': 'Person',
      };
    }
  }

  HadithHouse.HadithHouseApp.controller('UserPageCtrl',
    function ($scope, $rootScope, $location, $routeParams, UserResource) {
      let ctrl = new UserPageCtrl($scope, $rootScope, $location, $routeParams, UserResource);
      ctrl.initialize();
      return ctrl;
    });
}

