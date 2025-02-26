/** @type {import('ts-jest').JestConfigWithTsJest} **/
module.exports = {
  testEnvironment: './jest.environment.js',
  testEnvironmentOptions: {
    browsers: ['chrome', 'firefox', 'safari'],
    customExportConditions: [''],
  },
  transform: {
    '^.+\\.(ts|tsx)?$': 'ts-jest',
    '^.+\\.(js|jsx)$': 'babel-jest',
  },
  preset: 'ts-jest',
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },
  testPathIgnorePatterns: ['/node_modules/'],
  transformIgnorePatterns: [
    '[/\\\\]node_modules[/\\\\].+[^esm]\\.(js|jsx|mjs|cjs|ts|tsx)$',
    '^.+\\.module\\.(css|sass|scss)$',
    '/node_modules/(?!(@bundled-es-modules)/)',
  ],
  moduleNameMapper: {
    uuid$: 'uuid',
    '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$':
      '<rootDir>/src/fileMock.js',
    '\\.(css|less)$': '<rootDir>/src/styleMock.js',
  },
  roots: ['<rootDir>/src'],
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],
}
