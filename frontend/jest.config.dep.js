/** @type {import('ts-jest').JestConfigWithTsJest} **/
module.exports = {
  testEnvironment: 'jsdom',
  transformIgnorePatterns: [
    'node_modules/(?!axios|(?!msw)|.+[^esm])/',
    '[/\\\\]node_modules[/\\\\].+[^esm]\\.(js|jsx|mjs|cjs|ts|tsx)$',
    '/node_modules/(?!bundled-es-modules).+\\.js$',
    '/node_modules/(?!msw).+\\.js$',
  ],
  transform: {
    '^.+.tsx?$': ['ts-jest', {}],
  },
  moduleNameMapper: {
    // Force module uuid to resolve with the CJS entry point, because Jest does not support package.json.exports. See https://github.com/uuidjs/uuid/issues/451
    uuid: require.resolve('uuid'),
  },
  // moduleNameMapper: {
  //   '^axios$': 'axios/dist/node/axios.cjs',
  // },
}
