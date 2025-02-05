/*

Copyright (C) 2022 SE CookBook - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: help.cookbook@gmail.com

*/

import { MetricType } from "web-vitals";
 
const reportWebVitals = (onPerfEntry?: (metric: MetricType) => void) => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    import("web-vitals").then(({ onCLS, onINP, onFCP, onLCP, onTTFB }) => 
{
       onCLS(onPerfEntry);
       onINP(onPerfEntry);
       onFCP(onPerfEntry);
       onLCP(onPerfEntry);
       onTTFB(onPerfEntry);
     });
   }
 };

 export default reportWebVitals;