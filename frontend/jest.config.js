/** @type {import('ts-jest').JestConfigWithTsJest} **/
module.exports = {
  testEnvironment: 'jsdom',
  transformIgnorePatterns: ['node_modules/(?!axios)/'],
  transform: {
    '^.+.tsx?$': ['ts-jest', {}],
  },
  // moduleNameMapper: {
  //   '^axios$': 'axios/dist/node/axios.cjs',
  // },
}
