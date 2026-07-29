#include <fenv.h>
#include <fftw3.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static void audit_plan(const char *direction, int n, fftw_plan plan)
{
    double adds = 0.0;
    double muls = 0.0;
    double fmas = 0.0;
    char *description;

    if (plan == NULL) {
        fprintf(stderr, "failed to create %s plan for n=%d\n", direction, n);
        exit(2);
    }
    fftw_flops(plan, &adds, &muls, &fmas);
    description = fftw_sprint_plan(plan);
    if (description == NULL) {
        fprintf(stderr, "failed to describe %s plan for n=%d\n", direction, n);
        exit(2);
    }
    for (char *cursor = description; *cursor != '\0'; ++cursor) {
        if (*cursor == '\n' || *cursor == '\r' || *cursor == '\t')
            *cursor = ' ';
    }
    printf(
        "PLAN\t%s\t%d\t%.0f\t%.0f\t%.0f\t%.17g\t%s\n",
        direction,
        n,
        adds,
        muls,
        fmas,
        fftw_cost(plan),
        description
    );
    fftw_free(description);
}

int main(int argc, char **argv)
{
    int maximum_log2 = 18;
    const double pi = 3.141592653589793238462643383279502884;
    const double scaling = pow(2.0 * pi, 2.0) / 2.0;

    if (argc == 2)
        maximum_log2 = atoi(argv[1]);
    if (maximum_log2 < 0 || maximum_log2 > 24) {
        fprintf(stderr, "maximum_log2 must be in [0, 24]\n");
        return 2;
    }

    printf("META\tfftw_version\t%s\n", fftw_version);
    printf("META\tfftw_cc\t%s\n", fftw_cc);
    printf("META\tfftw_codelet_optim\t%s\n", fftw_codelet_optim);
    printf("META\trounding_mode\t%d\n", fegetround());
    printf("META\tplanner_flag\tFFTW_ESTIMATE\n");
    printf("META\tp2_scaling_hex\t%a\n", scaling);
    printf("META\tone_sixth_hex\t%a\n", 1.0 / 6.0);

    for (int log2_n = 0; log2_n <= maximum_log2; ++log2_n) {
        int n = 1 << log2_n;
        double *real_data = fftw_alloc_real((size_t)n);
        fftw_complex *complex_data =
            fftw_alloc_complex((size_t)(n / 2 + 1));
        fftw_plan forward;
        fftw_plan inverse;

        if (real_data == NULL || complex_data == NULL) {
            fprintf(stderr, "allocation failure for n=%d\n", n);
            return 2;
        }
        forward = fftw_plan_dft_r2c_1d(
            n, real_data, complex_data, FFTW_ESTIMATE);
        inverse = fftw_plan_dft_c2r_1d(
            n, complex_data, real_data, FFTW_ESTIMATE);
        audit_plan("r2c", n, forward);
        audit_plan("c2r", n, inverse);
        fftw_destroy_plan(forward);
        fftw_destroy_plan(inverse);
        fftw_free(complex_data);
        fftw_free(real_data);
    }
    fftw_cleanup();
    return 0;
}
