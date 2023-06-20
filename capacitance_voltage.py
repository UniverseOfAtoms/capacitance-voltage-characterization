from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np


class Fitting:
    def __init__(self, dataframes):
        self.tables = dataframes
        self.model = LinearRegression()
        self.temp = [187, 200, 250, 288, 300, 321, 350]

    def new_variable(self):
        for i, df in enumerate(self.tables):
            df["Temperature"] = self.temp[i]
            df["1/C2"] = 1/(df["Cp_AC"]**2)

    def capacitance_voltage_characteristic(self):
        self.new_variable()
        fig, ax = plt.subplots()
        for df in self.tables:
            ax.plot(df['DCV_AC'], df['Cp_AC'], label=f"{df['Temperature'][0]}K")
        ax.tick_params(direction='in', right=True, left=True, bottom=True, top=True)
        ax.set_xlabel('Voltage (V)')
        ax.set_ylabel('Capacitance (F)')
        ax.set_xlim(-12, 0)
        ax.legend()
        plt.show()

    def plot_1_c2_vs_v(self):
        self.new_variable()
        df_300 = self.tables[4]
        x = df_300["DCV_AC"]
        y = df_300["1/C2"]
        # Linear regression and calculation of r2
        self.model.fit(x.values.reshape(-1, 1),y)
        r2 = self.model.score(x.values.reshape(-1, 1), y)
        #print(r2)
        # Calculate Sum Squared Error SSE and degrees of freedom
        y_pred = self.model.predict(x.values.reshape(-1, 1))
        SSE = np.sum((y-y_pred)**2)
        df = len(x) - 2
        # Calculate mean squared error (MSE)
        MSE = SSE/df
        # Calculate sum of squares of x
        SSx = np.sum((x-np.mean(x))**2)
        # Calculate standard error of intercept and slope
        se_intercept = np.sqrt(MSE*(1/(len(x))+(np.mean(x)**2)/ SSx))
        se_slope = np.sqrt(MSE/SSx)
        #print(f"Standard Error of intercept: {se_intercept}, and Standard Error of slope: {se_slope}")

        Nd =format(-2/(1.6e-19*9.66*8.85e-12*1e-12*self.model.coef_[0]*1e6), ".2e")
        Vbi = round(-self.model.intercept_/self.model.coef_[0],2)
        #print(f"Netto donor concentration is {Nd}. Built-in potential is {Vbi}")

        # Plotting data and fitted line
        plt.scatter(x, y)
        plt.plot(x.values.reshape(-1, 1), self.model.intercept_ + self.model.coef_ * x.values.reshape(-1, 1),
                 color='red')
        plt.xlabel("Voltage (V)")
        plt.ylabel("1/C2 (F-2)")
        plt.figtext(0.54, 0.74, f"Nd={Nd}cm-3\nVbi={Vbi}eV", fontsize=10)
        plt.show()