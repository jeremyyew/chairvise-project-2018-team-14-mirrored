<template>
  <center>
    <div
      id="app"
      style="width:85%;"
    >
      <el-container id="main">
        <el-header
          id="main-header"
          height="90px"
        >
          <el-row
            type="flex"
            class="row-bg"
            justify="space-between"
            align="middle"
            style="height: inherit; line-height: 15px;"
          >
            <el-col :span="4" />
            <el-col
              :span="16"
            >
              <span
                id="app-title"
                :style="{marginTop: 30 }"
              >Conference Visualizer</span>
            </el-col>
            <el-col
              id="sign-in-col"
              :span="4"
            >
              <el-button
                v-if="!isAuthenticated"
                id="sign-in"
                type="primary"
                @click="authDialogOpen = true"
              >
                Log In
              </el-button>
              <el-button
                v-if="isAuthenticated"
                id="sign-out"
                type="primary"
                @click="logout"
              >
                Log Out ({{ username }})
              </el-button>
              <el-dialog
                title="Log in or Sign Up"
                :visible.sync="authDialogOpen"
                width="50%"
              >
                <el-tabs
                  v-model="loginFormActiveTabName"
                  :stretch="true"
                >
                  <el-tab-pane
                    label="Log In"
                    name="loginTab"
                  >
                    <el-form
                      ref="loginForm"
                      v-loading="isLoginLoading"
                      :rules="loginRules"
                      :model="loginForm"
                      label-width="120px"
                    >
                      <el-form-item
                        label="Username"
                        prop="username"
                      >
                        <el-input v-model="loginForm.username" />
                      </el-form-item>
                      <el-form-item
                        label="Password"
                        prop="password"
                      >
                        <el-input
                          v-model="loginForm.password"
                          type="password"
                        />
                      </el-form-item>
                      <el-form-item>
                        <el-button
                          type="primary"
                          class="btn-block"
                          @click="login"
                        >
                          Login
                        </el-button>
                      </el-form-item>
                      <el-form-item>
                        <div class="side-line">or</div>
                      </el-form-item>
                      <el-form-item>
                        <el-button
                          type="primary"
                          class="btn-facebook btn-block"
                          icon="fab fa-facebook"
                          @click="authenticate('facebook')"
                        >
                          Login with Facebook
                        </el-button>
                      </el-form-item>
                      <el-form-item>
                        <el-button
                          type="primary"
                          class="btn-google btn-block"
                          icon="fab fa-google"
                          @click="authenticate('google')"
                        >
                          Login with Google
                        </el-button>
                      </el-form-item>
                      <el-form-item>
                        <el-button
                          type="primary"
                          class="btn-github btn-block"
                          icon="fab fa-github"
                          @click="authenticate('github')"
                        >
                          Login with Github
                        </el-button>
                      </el-form-item>
                    </el-form>
                  </el-tab-pane>
                  <el-tab-pane
                    label="Sign Up"
                    name="signupTab"
                  >
                    <el-form
                      ref="registerForm"
                      v-loading="isRegistrationLoading"
                      :rules="registerRules"
                      :model="registerForm"
                      label-width="120px"
                    >
                      <el-form-item
                        label="Email"
                        prop="email"
                      >
                        <el-input
                          v-model="registerForm.email"
                          type="email"
                        />
                      </el-form-item>
                      <el-form-item
                        label="Username"
                        prop="username"
                      >
                        <el-input
                          v-model="registerForm.username"
                        />
                      </el-form-item>
                      <el-form-item
                        label="Password"
                        prop="password"
                      >
                        <el-input
                          v-model="registerForm.password"
                          type="password"
                        />
                      </el-form-item>
                      <el-form-item
                        label="Confirm"
                        prop="checkPassword"
                      >
                        <el-input
                          v-model="registerForm.checkPassword"
                          type="password"
                        />
                      </el-form-item>
                      <el-form-item>
                        <el-button
                          type="primary"
                          class="btn-block"
                          @click="register"
                        >
                          Sign Up
                        </el-button>
                      </el-form-item>
                    </el-form>
                  </el-tab-pane>
                </el-tabs>

                <span
                  slot="footer"
                  class="dialog-footer"
                />
              </el-dialog>
            </el-col>
          </el-row>
        </el-header>
        <el-container>
          <el-aside style="width:20%;">
            <!--<router-link to="/">-->
            <!--<el-button @click="startHacking" type="primary">Start</el-button>-->
            <!--</router-link>-->
            <!--<router-link to="/chart" :chartData="testChartsDataInput">-->
            <!--<el-button type="selection">Chart</el-button>-->
            <!--</router-link>-->
            <!--router-link to="/ec">
              <el-button type="success">EC</el-button>
            </router-link-->
            <!--<router-link to="/te">-->
            <!--<el-button type="success">WY</el-button>-->
            <!--</router-link>-->
            <MappingHeaderDialog
              :mapping-data="mappingAuthorData"
              :data-type-name="'mappingAuthorData'"
              @dataProcessSuccess="updateResultData"
              @dataProcessFailed="handleError"
            />
            <MappingHeaderDialog
              :mapping-data="mappingSubmissionData"
              :data-type-name="'mappingSubmissionData'"
              @dataProcessSuccess="updateResultData"
              @dataProcessFailed="handleError"
            />
            <MappingHeaderDialog
              :mapping-data="mappingReviewData"
              :data-type-name="'mappingReviewData'"
              @dataProcessSuccess="updateResultData"
              @dataProcessFailed="handleError"
            />
            <center id="upload">
              <form
                v-if="isInitial || isSaving || isSuccess"
                enctype="multipart/form-data"
                novalidate
              >
                <!--The type multipart/form-data is important, otherwise Django will not accept-->
                <h2>Upload Files</h2>
                <h4>Drag files into their respective boxes, or click to browse</h4>
                <div class="dropbox">
                  <input
                    type="file"
                    :name="uploadFieldName"
                    :disable="isSaving"
                    accept=".csv"
                    class="input-author-file"
                    @change="uploadCSV($event.target.name, $event.target.files,
                                       'mappingAuthorData')"
                  >
                  <p style="margin-bottom:0px;padding-top:32px;font-size:18px">
                    <strong>author.csv</strong>
                  </p>
                </div>
                <div class="dropbox">
                  <input
                    type="file"
                    :name="uploadFieldName"
                    :disable="isSaving"
                    accept=".csv"
                    class="input-submission-file"
                    @change="uploadCSV($event.target.name, $event.target.files,
                                       'mappingSubmissionData')"
                  >
                  <p style="margin-bottom:0px;padding-top:32px;font-size:18px">
                    <strong>submission.csv</strong>
                  </p>
                </div>
                <div class="dropbox">
                  <input
                    type="file"
                    :name="uploadFieldName"
                    :disable="isSaving"
                    accept=".csv"
                    class="input-review-file"
                    @change="uploadCSV($event.target.name, $event.target.files,
                                       'mappingReviewData')"
                  >
                  <p style="margin-bottom:0px;padding-top:32px;font-size:18px">
                    <strong>review.csv</strong>
                  </p>
                </div>
              </form>
            </center>
          </el-aside>
          <el-main>
            <ResultTabs
              :result="result"
              :last-updated-viz="lastUpdatedViz"
            />
            <el-row
              type="flex"
            >
              <el-button
                type="success"
                style="margin-top: 10px"
                :icon="pdfIcon"
                @click="generatePdf"
              >Save all as PDF
              </el-button>
            </el-row>
          </el-main>
        </el-container>
        <el-footer id="main-footer">
          <el-row
            type="flex"
            class="row-bg"
            justify="space-between"
            style="height: inherit"
          >
            <el-col :span="4" />
            <el-col :span="12" />
            <el-col :span="4">
              <img
                src="./assets/logo.png"
                style="vertical-align: middle;width: 20px; "
              >
            </el-col>
          </el-row>
        </el-footer>
      </el-container>
    </div>
  </center>

</template>

<script>
import ResultTabs from '@/components/ResultTabs';
import Auth from '@/components/Auth';
import StorePersisted from '@/storePersisted';
import Store from '@/store';
import utils from '@/utils';
import axios from 'axios';
import jwt_decode from 'jwt-decode';
import Const from '@/components/Const';
import { upload } from './components/Upload';
import MappingHeaderDialog from './components/MappingHeaderDialog';

const STATUS_INITIAL = 0;
const STATUS_SAVING = 1;
const STATUS_SUCCESS = 2;
const STATUS_FAILED = 3;

const { stringify } = utils;
const { CHART_IDS } = Const;

const REFRESH_TOKEN_MS = 15 * 60 * 1000;
let refreshTokenTimer;

export default {
  name: 'App',
  components: { MappingHeaderDialog, ResultTabs },
  data() {
    const validatePassword = (rule, value, callback) => {
      if (this.registerForm.checkPassword !== '') {
        this.$refs.registerForm.validateField('checkPassword');
      }
      callback();
    };
    const validateCheckPassword = (rule, value, callback) => {
      if (value !== this.registerForm.password) {
        callback(new Error('Please confirm your password again because it is not matching.'));
      } else {
        callback();
      }
    };
    return {
      isSavingPdf: false,
      storePersistedState: StorePersisted.state,
      authDialogOpen: false,
      isRegistrationLoading: false,
      isLoginLoading: false,
      isAuthenticated: this.$auth.isAuthenticated(),
      username: this.$auth.isAuthenticated() ? jwt_decode(this.$auth.getToken()).username : null,
      loginFormActiveTabName: 'loginTab',
      loginForm: {
        username: '',
        password: '',
      },
      loginRules: {
        username: [
          {
            required: true,
            message: 'Please input a username',
            trigger: 'blur',
          },
        ],
        password: [
          {
            required: true,
            message: 'Please input a password',
            trigger: 'blur',
          },
        ],
      },
      registerForm: {
        email: '',
        username: '',
        password: '',
        checkPassword: '',
      },
      registerRules: {
        email: [
          {
            required: true,
            message: 'Please input an email address',
            trigger: 'blur',
          },
          {
            type: 'email',
            message: 'Please input a valid email',
            trigger: 'blur',
          },
        ],
        username: [
          {
            required: true,
            message: 'Please input a username',
            trigger: 'blur',
          },
        ],
        password: [
          {
            required: true,
            message: 'Please input a password',
            trigger: 'blur',
          },
          {
            validator: validatePassword,
            trigger: 'blur',
          },
        ],
        checkPassword: [
          {
            required: true,
            message: 'Please confirm your password',
            trigger: 'blur',
          },
          {
            validator: validateCheckPassword,
            trigger: 'blur',
          },
        ],
      },
      uploadedFiles: [],
      uploadError: null,
      currentStatus: null,
      uploadFieldName: 'file',
      testChartsDataInput: null,
      result: {
        author: {},
        review: {},
        submission: {},
      },
      mappingAuthorData: {
        placeHolder: [],
        previewData: [],
        numCols: 0,
        minCols: 4,
        defaultMinCol: 6,
        dialogOpen: false,
        methodName: 'getAuthorInfo',
        fileID: '.input-author-file',
        defaultUploadForm: {
          firstNameIndex: 1,
          lastNameIndex: 2,
          countryIndex: 4,
          affiliationIndex: 5,
        },
        initialUploadForm: {
          firstNameIndex: -1,
          lastNameIndex: -1,
          countryIndex: -1,
          affiliationIndex: -1,
        },
        uploadForm: {
          firstNameIndex: -1,
          lastNameIndex: -1,
          countryIndex: -1,
          affiliationIndex: -1,
        },
        options: [
          {
            value: 'firstNameIndex',
            label: 'First Name',
          },
          {
            value: 'lastNameIndex',
            label: 'Last Name',
          },
          {
            value: 'countryIndex',
            label: 'Country',
          },
          {
            value: 'affiliationIndex',
            label: 'Affiliation',
          },
        ],
      },
      mappingSubmissionData: {
        placeHolder: [],
        previewData: [],
        numCols: 0,
        minCols: 6,
        defaultMinCol: 10,
        dialogOpen: false,
        methodName: 'getSubmissionInfo',
        fileID: '.input-submission-file',
        defaultUploadForm: {
          trackNameIndex: 2,
          authorIndex: 4,
          submissionTimeIndex: 5,
          lastEditTimeIndex: 6,
          keywordIndex: 8,
          decisionIndex: 9,
        },
        initialUploadForm: {
          trackNameIndex: -1,
          authorIndex: -1,
          submissionTimeIndex: -1,
          lastEditTimeIndex: -1,
          keywordIndex: -1,
          decisionIndex: -1,
        },
        uploadForm: {
          trackNameIndex: -1,
          authorIndex: -1,
          submissionTimeIndex: -1,
          lastEditTimeIndex: -1,
          keywordIndex: -1,
          decisionIndex: -1,
        },
        options: [
          {
            value: 'trackNameIndex',
            label: 'Track Name',
          },
          {
            value: 'authorIndex',
            label: 'Author',
          },
          {
            value: 'submissionTimeIndex',
            label: 'Submission Time',
          },
          {
            value: 'lastEditTimeIndex',
            label: 'Last Edit Time',
          },
          {
            value: 'keywordIndex',
            label: 'Keyword',
          },
          {
            value: 'decisionIndex',
            label: 'Decision',
          },
        ],
      },
      mappingReviewData: {
        placeHolder: [],
        previewData: [],
        numCols: 0,
        minCols: 2,
        defaultMinCol: 7,
        dialogOpen: false,
        methodName: 'getReviewInfo',
        fileID: '.input-review-file',
        defaultUploadForm: {
          submissionIDIndex: 1,
          evaluationIndex: 6,
        },
        initialUploadForm: {
          submissionIDIndex: -1,
          evaluationIndex: -1,
        },
        uploadForm: {
          submissionIDIndex: -1,
          evaluationIndex: -1,
        },
        options: [
          {
            value: 'submissionIDIndex',
            label: 'Submission ID',
          },
          {
            value: 'evaluationIndex',
            label: 'Evaluation',
          },
        ],
      },
      lastUpdatedViz: { value: 'author' },
      options: [
        {
          value: 'author',
          label: 'Author File',
        }, {
          value: 'submission',
          label: 'Submission File',
        }, {
          value: 'review',
          label: 'Review File',
        },
      ],
    };
  },
  computed: {
    pdfIcon() {
      return this.isSavingPdf ? 'el-icon-loading' : 'el-icon-download';
    },
    isInitial() {
      return this.currentStatus === STATUS_INITIAL;
    },
    isSaving() {
      return this.currentStatus === STATUS_SAVING;
    },
    isSuccess() {
      return this.currentStatus === STATUS_SUCCESS;
    },
    isFailed() {
      return this.currentStatus === STATUS_FAILED;
    },
  },
  watch: {
  },
  created() {
    // console.log(`StorePersisted.state: ${stringify(StorePersisted.state)}`);
    // console.log(`storePersistedState: ${stringify(this.storePersistedState)}`);
    this.$persist(['storePersistedState']);
    if (this.$auth.getToken() !== null) {
      this.refreshToken();
    }
  },
  mounted() {
    this.reset();
  },
  methods: {
    // startHacking() {
    //   this.$notify({
    //     title: 'It works!',
    //     type: 'success',
    //     message: 'We\'ve laid the ground work for you.',
    //     duration: 2500,
    //   });
    // },
    async generatePdf() {
      const pdfGenerator = new utils.PdfGenerator();
      this.isSavingPdf = true;
      // try {
      await pdfGenerator.generate(
        [
          CHART_IDS.TOP_SUBMITTED_AFFILIATION_BAR_PIE_ID,
          CHART_IDS.TOP_AUTHOR_BAR_ID,
          CHART_IDS.TOP_COUNTRY_BAR_ID,
          CHART_IDS.TOP_SUBMITTED_AFFILIATION_BAR_PIE_ID,
          CHART_IDS.SUBMISSION_TIME_SERIES_ID,
          CHART_IDS.HISTORICAL_ACCEPTANCE_ID,
          CHART_IDS.ACCEPTANCE_BY_TRACK_ID,
          CHART_IDS.TOP_ACCEPTED_AUTHORS_ID,
          CHART_IDS.TOP_ACCEPTED_AUTHORS_BY_TRACK_ID,
          CHART_IDS.SUBMISSIONS_WORD_CLOUD_ALL_ID,
          CHART_IDS.SUBMISSIONS_WORD_CLOUD_ACCEPTED_ID,
          CHART_IDS.SUBMISSIONS_WORD_CLOUD_BY_TRACK_ID,
        ],
      );
      // } catch (err) {
      //   this.$notify({
      //     title: 'Error printing pdf',
      //     type: 'error',
      //     message: err,
      //     duration: 2500,
      //   });
      //   this.isSavingPdf = false;
      // }
      this.isSavingPdf = false;
    },
    setUserAuthenticated() {
      this.isAuthenticated = true;
      this.username = jwt_decode(this.$auth.getToken()).username;
      refreshTokenTimer = setTimeout(this.refreshToken, REFRESH_TOKEN_MS);

      axios.post(process.env.VUE_APP_API_BASE_URL + process.env.VUE_APP_ANALYZE_DATA_URL)
        .then((response) => {
          response.data.data.forEach((data) => {
            const result = {
              inputFileName: `${data.infoType}.csv`,
              chartData: data.infoData,
            };
            this.updateResultData(data.infoType, result, false);
          });
        })
        .catch(() => {
          this.$message({
            message: 'Unable to retrieve data. Please try again later.',
            type: 'error',
          });
        });
    },
    login() {
      this.$refs.loginForm.validate((valid) => {
        if (!valid) {
          return false;
        }
        this.isLoginLoading = true;
        this.$auth.login(this.loginForm)
          .then(() => {
            this.setUserAuthenticated();
            this.authDialogOpen = false;
          })
          .catch((error) => {
            const errorMessage = error.response.data.non_field_errors[0];

            this.$message({
              message: errorMessage !== undefined ? errorMessage : 'Unexpected login failure. Please try again later.',
              type: 'error',
            });
          })
          .finally(() => {
            this.isLoginLoading = false;
          });

        return true;
      });
    },
    register() {
      this.$refs.registerForm.validate((valid) => {
        if (!valid) {
          return false;
        }

        this.isRegistrationLoading = true;
        this.$auth.register({
          username: this.registerForm.username,
          email: this.registerForm.email,
          password: this.registerForm.password,
        })
          .then((response) => {
            this.$message({
              message: 'Sign up successful!',
              type: 'success',
            });
            // TODO: trigger login automatically?
          })
          .catch((error) => {
            this.$message({
              message: error.response.data.detail,
              type: 'error',
            });
          })
          .finally(() => {
            this.isRegistrationLoading = false;
          });
        return true;
      });
    },
    refreshToken() {
      axios.post(process.env.VUE_APP_API_BASE_URL + process.env.VUE_APP_TOKEN_REFRESH_URL,
        { token: this.$auth.getToken() })
        .then(() => {
          this.setUserAuthenticated();
        })
        .catch(() => {
          this.logout();
        });
    },
    authenticate(provider) {
      // Auth.authenticate(provider);
      // Store.login('jeremy.yew@u.yale-nus.edu.sg');
      this.isLoginLoading = true;
      this.$auth.authenticate(provider, { provider: provider === 'google' ? 'google-oauth2' : provider })
        .then(() => {
          this.setUserAuthenticated();
          this.authDialogOpen = false;
          this.isLoginLoading = false;
        })
        .catch((error) => {
          // We want to use finally to set the login loading to false.
          // However, the promise here is a custom implementation and has no finally.
          this.isLoginLoading = false;
          console.log(error);
        });
    },
    logout() {
      // Store.logout();
      this.$auth.logout()
        .then(() => {
          clearTimeout(refreshTokenTimer);
          this.isAuthenticated = false;
          // Because we want to allow calling logout at any point of time, e.g. during create,
          // this (and child) components might not have been mounted yet
          this.$nextTick(() => {
            this.$message({
              message: 'You have been signed out!',
              type: 'warning',
            });
          });
        })
        .catch((error) => {
          console.log(`Failed to log out: ${error}`);
        });
    },
    reset() {
      // reset form to initial state
      this.currentStatus = STATUS_INITIAL;
      this.uploadedFiles = [];
      this.uploadError = null;
    },
    updateResultData(infoType, result, switchTab = true) {
      this.currentStatus = STATUS_SUCCESS;
      if (switchTab) {
        Store.switchActiveTab(infoType);
      }
      this.result[infoType] = result;
    },
    handleError(err) {
      this.uploadError = err.response;
      this.currentStatus = STATUS_FAILED;
    },
    uploadCSV(fieldName, fileList, dataField) {
      if (!fileList.length) return;

      this.currentStatus = STATUS_SAVING;

      const formData = new FormData();
      Array
        .from(Array(fileList.length)
          .keys())
        .map((x) => {
          formData.append(fieldName, fileList[x], fileList[x].name);
        });

      upload(formData, 'parse')
        .then((x) => {
          this[dataField].numCols = Object.keys(x.previewData[0]).length;
          if (this[dataField].numCols < this[dataField].minCols) {
            this.$message({
              message: '.csv file provided does not contain enough columns for processing!',
              type: 'error',
            });
            document.querySelector(this[dataField].fileID).value = '';
            return;
          }

          this[dataField].defaultUploadForm.sessionId = x.sessionId;
          this[dataField].uploadForm.sessionId = x.sessionId;

          this[dataField].previewData = x.previewData;
          this[dataField].dialogOpen = true;
        })
        .catch((err) => {
          this.uploadError = err.response;
          this.currentStatus = STATUS_FAILED;
          document.querySelector(this[dataField].fileID).value = '';
        });
    },
  },
};

</script>

<style lang="scss">
  @import "@fortawesome/fontawesome-free/css/brands.css";
  @import "@fortawesome/fontawesome-free/css/fontawesome.css";
  $content-padding: 20px;
  $element-shadow: 0 2px 4px 0 rgba(0,0,0,.12),0 0 6px 0 rgba(0,0,0,.04);
  #upload {
  }

  .dropbox {
    outline: 2px dashed grey; /* the dash box */
    outline-offset: -10px;
    background: lightcyan;
    color: dimgray;
    /*padding: 10px 10px;*/
    height: 100px; /* minimum height */
    width: 90%;
    position: relative;
    cursor: pointer;
  }

  .input-author-file {
    opacity: 0; /* invisible but it's there! */
    width: 100%;
    height: 100%;
    position: absolute;
    cursor: pointer;
    left: 0; /*put this otherwise the input box will shift by half of the parent width */
  }

  .input-submission-file {
    opacity: 0; /* invisible but it's there! */
    width: 100%;
    height: 100%;
    position: absolute;
    cursor: pointer;
    left: 0; /*put this otherwise the input box will shift by half of the parent width */
  }

  .input-review-file {
    opacity: 0; /* invisible but it's there! */
    width: 100%;
    height: 100%;
    position: absolute;
    cursor: pointer;
    left: 0; /*put this otherwise the input box will shift by half of the parent width */
  }

  .dropbox:hover {
    background: lightblue; /* when mouse over to the drop zone, change color */
  }

  .dropbox p {
    font-size: 1.2em;
    text-align: center;
    padding: 50px 0;
  }

  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    width: 100% !important;
    /*margin-top: 30px;*/
  }

  #main {
    /*margin-bottom: 20px;*/
  }

  .el-header,
  .el-footer {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
    /*margin-bottom: 5px;*/
  }

  .el-aside {
    padding: $content-padding;
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 30px;
    /*margin-right: 5px;*/
  }

  .el-main {
    background-color: #E9EEF3;
    color: #333;
    height: 800px;
    /*text-align: center;*/
    /*line-height: 450px;*/
  }

  body {
    margin: 0;
  }

  body > .el-container {
    /*margin-bottom: 40px;*/
  }

  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }

  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }

  #sign-in {
  }

  #sign-in-col {
  }

  #app-title-col {

  }

  #app-title {
    font-weight: bolder;
    font-size: 30px;
    margin-top: 50px;
  }

  #main-header {
    z-index: 1000;
    position: sticky;
    top: 0;
    box-shadow: $element-shadow;
  }

  #main-footer {
    position: sticky;
    bottom: 0;
    box-shadow: $element-shadow;
  }

  .side-line {
    display: flex;
    flex-direction: row;
  }

  .side-line:before, .side-line:after {
    content: "";
    flex: 1 1;
    border-bottom: 1px solid rgba(0,0,0,.2);
    margin:auto .5em;
  }

  .btn-block {
    width: 100%;
  }

  .btn-facebook {
    border: 0;
    background-color: #4267b2;
  }
  .btn-facebook:hover, .btn-facebook:focus {
    background-color: #3b5291;
  }
  .btn-google {
    border: 0;
    background-color: #4285f4;
  }
  .btn-google:hover, .btn-google:focus {
    background-color: #426fde;
  }
  .btn-github {
    border: 0;
    background-color: #333333;
  }
  .btn-github:hover, .btn-github:focus {
    background-color: #555555;
  }
</style>
